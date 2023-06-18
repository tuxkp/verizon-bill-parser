import json
import sys
from pdfminer.high_level import extract_text

if len(sys.argv) < 2:
  print('Usage: vzw.py <bill_name.pdf>')
  exit(1)

print(sys.argv[1])

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTAnno, LTPage

data = {}

skipPageText = [
    "Questions about your bill?",
    "Talk activity",
    "Talk activity (cont.)",
    "Customer Proprietary Network Information",
    "Additional information continued"
]

fields = {
    "billingPeriod": {
        "label": "Billing period",
        "page": 0,
        # "xy": {
        #     "x": 0,
        #     "y": 0
        # }
    }
}

def parse_element(eltype: str, pageNumber: int, element) -> dict:
    elementText = element.get_text()
    #Remove \n from element text
    elementText = elementText.replace("\n", "")

    if eltype == "TextLine":
        print("pageNumber="+str(pageNumber)+",TextLine=" + elementText + ",x=" + str(round(element.x0, 2)) + ",y=" + str(round(element.y0, 2)))
        #Loop though fields dict and find if the key is in data dict
        #If it is, then add the text to the data dict
        #If it is not, then ignore it
        for key in fields:
            field = fields[key]
            if key not in data and field["page"] == pageNumber:
                #Check if element text contains label
                if field["label"] in elementText:    
                    #Check if field contains x and y
                    if "xy" in field:
                        #Check if element is within x and y
                        if element.x0 >= field["xy"]["x"] and element.y0 >= field["xy"]["y"]:
                            data[key] = elementText
                    else:
                        data[key] = elementText

    return {
        type: eltype,
        "xy": {
            "x": round(element.x0, 2),
            "y": round(element.y0, 2)
        },
        "subElements": []
    }

def parse_page(page: LTPage, pageNumber: int) -> list:
    parsedPageElements = []
    for pageElement in page:
        if isinstance(pageElement, LTTextContainer):
            parsedElement = parse_element("TextContainer", pageNumber, pageElement)
            for text_line in pageElement:
                if not isinstance(text_line, LTAnno):
                    line = parse_element("TextLine", pageNumber, text_line)
                    line["text"] = text_line.get_text()
                    parsedElement["subElements"].append(line)
                    if text_line.get_text().replace("\n", "") in skipPageText:
                        return parsedPageElements
            parsedPageElements.append(parsedElement)
    return parsedPageElements

def parse_pdf(filePath) -> list:
    pages = []
    pageNumber = 0
    for page_layout in extract_pages(filePath):
        page = parse_page(page_layout, pageNumber)
        pages.append(page)
        pageNumber += 1
    return pages

pages = parse_pdf(sys.argv[1])

print(json.dumps(pages))