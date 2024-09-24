#Class MyPDFUtils
from pdfminer.high_level import extract_text, extract_pages, LTPage
import os
from datetime import datetime

class MyPDFUtils:

    def __init__(self, pdf_file_name):
        self.vzwPdfVersions = {
            "v1": {
                "dateInit": "01/01/2022",
                "dateEnd": "12/01/2022",
                "pagesToParse": [0],
                "coordinateMaxLimits": {
                    "x1": 385
                },
                "contextMap": {
                    ".": {
                        "final": "abcd",
                        "skip": [
                            "am a test",
                            "Smartphone"
                        ],
                        "callback": self.v1_parseCharges
                    }
                }
            },
            "v2": {
                "dateInit": "01/01/2024",
                "dateEnd": "09/01/2024",
                "detectVersionFromContent": {
                    "page": 0,
                    "text": "Bill date\nAccount number\nInvoice number\n",
                    "x0": 276,
                    "y0": 215,
                },
                "pagesToParse": [2],
                "contextMap": {
                    "Bill summary by line": {
                        "final": "abcd",
                        "skip": [
                            "am a test",
                            "Smartphone",
                            "Questions about your bill?\nverizon.com/support\n800-922-0204",
                            "Review your bill online",
                            "An itemized bill breakdown of all\ncharges and credits is available on\nthe My Verizon app and online.",
                            "Scan the QR code\nwith your camera\napp or go to\ngo.vzw.com/bill.",
                            "Surcharges, taxes and gov fees"
                        ],
                        "callback": self.v2_parseChargesByLineSummary
                    }
                }
            }
        }

        self.parsedData = {
            "amounts": [],
            "account": None,
            "invoice": None,
        }
        self.currentContext = None
        self.amountIndex = 0
        self.pdf_file_name = pdf_file_name
        self.pdf_file_name_without_folder = self.pdf_file_name.split(os.sep)[-1]
        self.pdf_file_version = self.get_file_version()
        self.extract_pages()
        self.parse_data_elements()
    
    def get_file_version_from_filename(self):
        #Extract date from file name
        dateParts = self.pdf_file_name_without_folder.split("_")[1].split(".")
        #Date object
        date = datetime(int(dateParts[2]), int(dateParts[0]), int(dateParts[1]))
        #Check if date is within the range of any version
        for version in self.vzwPdfVersions:
            dateInit = datetime.strptime(self.vzwPdfVersions[version]["dateInit"], "%m/%d/%Y")
            dateEnd = datetime.strptime(self.vzwPdfVersions[version]["dateEnd"], "%m/%d/%Y")
            if date >= dateInit and date <= dateEnd:
                return version
        return None
    
    def get_file_version_from_content(self) -> str:
        for version in self.vzwPdfVersions:
            if "detectVersionFromContent" in self.vzwPdfVersions[version]:
                detectObj = self.vzwPdfVersions[version]["detectVersionFromContent"]
                pageNumber = detectObj["page"]
                for page_layout in extract_pages(self.pdf_file_name, page_numbers=[pageNumber]):
                    for element in page_layout:
                        if element.__class__.__name__ == "LTTextBoxHorizontal":
                            elementX0Floor = int(element.x0)
                            elementY0Floor = int(element.y0)
                            if elementX0Floor == detectObj["x0"] and elementY0Floor == detectObj["y0"] \
                                and element.get_text() == detectObj["text"]:
                                return version         
        return None
        
    def get_file_version(self):
        '''
        File name should be in the format MyBill_MM.DD.YYYY.pdf
        extract the date from the file name and return the version of the file
        by looking up the date in the vzwPdfVersions dictionary
        '''
        #Check if the file is a PDF file
        if not self.pdf_file_name.endswith(".pdf"):
            raise Exception(f"File {self.pdf_file_name} is not a PDF file")
        
        #Check if the file name is in the MyBill_MM.DD.YYYY.pdf format
        if not self.pdf_file_name_without_folder.startswith("MyBill_"):
            return self.get_file_version_from_content()
        else:
            return self.get_file_version_from_filename()

    def extract_pages(self):
        self.pdf_extracted_pages: list[LTPage] = []
        for pagenumber in self.vzwPdfVersions[self.pdf_file_version]["pagesToParse"]:
            for page_layout in extract_pages(self.pdf_file_name, page_numbers=[pagenumber]):
                self.pdf_extracted_pages.append(page_layout)
                print("Page Number: " + str(pagenumber))

    def parse_data_elements(self):
        for page in self.pdf_extracted_pages:
            for element in page:
                if element.__class__.__name__ == "LTTextContainer":
                    self.parse_element("TextLine", element)
                elif element.__class__.__name__ == "LTTextBoxHorizontal":
                    self.parse_element("TextBox", element)
                elif element.__class__.__name__ == "LTChar":
                    self.parse_element("Char", element)
                elif element.__class__.__name__ == "LTAnno":
                    self.parse_element("Anno", element)
    
    def parse_element(self, eltype: str, element):
        elementText = element.get_text()
        #If the last two characters of elementText are \n then remove them
        if elementText[-1:] == "\n":
            elementText = elementText[:-1]
        
        if eltype == "TextBox":
            print("TextBox=" + elementText)
            if self.currentContext == None and elementText in self.vzwPdfVersions[self.pdf_file_version]["contextMap"]:
                self.currentContext = elementText
                print("Context: " + self.currentContext)
            elif self.currentContext != None and elementText == self.vzwPdfVersions[self.pdf_file_version]["contextMap"][self.currentContext]["final"]:
                del self.vzwPdfVersions[self.pdf_file_version]["contextMap"][self.currentContext]
                self.currentContext = None
                print("Context: None")
            elif self.currentContext != None and \
                "callback" in self.vzwPdfVersions[self.pdf_file_version]["contextMap"][self.currentContext] \
                and elementText not in self.vzwPdfVersions[self.pdf_file_version]["contextMap"][self.currentContext]["skip"]:
                self.vzwPdfVersions[self.pdf_file_version]["contextMap"][self.currentContext]["callback"](elementText, element)

        print("Element Type: " + eltype)
        
    def v2_parseChargesByLineSummary(self, elementText, element):
        if elementText.startswith("Billing period"):
            self.parsedData["billingPeriod"] = elementText.split(":")[1].strip()
        elif elementText.startswith("Account:"):
            '''
            Account: 324XXXXXX-00001  \nInvoice: 8695XXXXXX\nBilling period: Jun 19 - Jul 18, 2024
            '''
            self.parsedData["account"] = elementText.split("\n")[0].split(":")[1].strip()
            self.parsedData["invoice"] = elementText.split("\n")[1].split(":")[1].strip()
        elif elementText.startswith("The total amount due for this month"):
            pass
        elif elementText.startswith("$"):
            self.parsedData["amounts"][self.amountIndex]["amount"] = elementText
            self.amountIndex += 1
        else:
            self.parsedData["amounts"].append(
                {
                    "description": elementText,
                    "amount": None
                }
            )
        
    def v1_parseCharges(self, elementText, element):
        if not self.checkCoordinateLimits(element):
            return
    
        print("v1_parseCharges: " + elementText)
        if elementText.startswith("$"):
            self.parsedData["amounts"][self.amountIndex]["amount"] = elementText
            self.amountIndex += 1
        else:
            self.parsedData["amounts"].append(
                    {
                        "description": elementText,
                        "amount": None
                    }
                )

    def checkCoordinateLimits(self, element):
        if "coordinateMaxLimits" in self.vzwPdfVersions[self.pdf_file_version]:
            if element.x1 > self.vzwPdfVersions[self.pdf_file_version]["coordinateMaxLimits"]["x1"]:
                return False
        return True