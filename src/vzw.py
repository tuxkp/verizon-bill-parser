import json
import sys
from pdfminer.high_level import extract_text

if len(sys.argv) < 2:
  print('Usage: vzw.py <bill_name.pdf>')
  exit(1)

print(sys.argv[1])

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTAnno, LTPage

dataDict = {
    "currentContext": None
}

def parseChargesByLineSummary(textLine: str, x: float, y: float, height: float):
    if x > 400:
        return
    if "chargesByLineSummary" not in dataDict:
        dataDict["chargesByLineSummary"] = {}
    
    print("TextLine=" + textLine +",Height=" + str(height) + ",x=" + str(x) + ",y=" + str(y))
    if "Account" in textLine:
        dataDict["accountNumber"] = textLine.split(":")[1].strip()
    elif "Billing period" in textLine:
        dataDict["billingPeriod"] = textLine.split(":")[1].strip()
    elif "Invoice" in textLine:
        dataDict["invoiceNumber"] = textLine.split(":")[1].strip()
    elif height == 10.0 and x == 39.6:
        #If TextLine matches phone number format
        if textLine[3] == "-" and textLine[7] == "-":
            dataDict["chargesByLineSummary"][dataDict["chargesByLineSummary"]["currentY"]]["phoneNumber"] = textLine.strip()
        else:
            if str(y) not in dataDict["chargesByLineSummary"]:
                dataDict["chargesByLineSummary"][str(y)] = {}
            dataDict["chargesByLineSummary"]["currentY"] = str(y)
            dataDict["chargesByLineSummary"][str(y)]["name"] = textLine.strip()
    elif x > 300 and x < 400:
        if str(y) not in dataDict["chargesByLineSummary"]:
                dataDict["chargesByLineSummary"][str(y)] = {}
        dataDict["chargesByLineSummary"][str(y)]["amount"] = textLine.strip()
    
contextMap = {
    "Charges by line summary": {
        "final": "Total:",
        "skip": [
            "am a test",
            "Smartphone"
        ],
        "callback": parseChargesByLineSummary
    }
}

def parse_element(eltype: str, pageNumber: int, element, data:dict) -> dict:
    elementText = element.get_text()
    #Remove \n from element text
    elementText = elementText.replace("\n", "")

    if eltype == "TextLine":
        x = round(element.x0,2)
        y = round(element.y0,2)
        height = round(element.height,2)
        print("TextLine=" + elementText +",Height=" + str(height) + ",x=" + str(x) + ",y=" + str(y))
        if data['currentContext'] == None and elementText in contextMap:
            data['currentContext'] = elementText
            print("Context: " + data['currentContext'])
        elif data['currentContext'] != None and elementText == contextMap[data['currentContext']]["final"]:
            del contextMap[data['currentContext']]
            data['currentContext'] = None
            print("Context: None")
        elif data['currentContext'] != None and \
            "callback" in contextMap[data['currentContext']] \
            and elementText not in contextMap[data['currentContext']]["skip"]:
            contextMap[data['currentContext']]["callback"](elementText, x, y, height)


def parse_page(page: LTPage, pageNumber: int, data: dict) -> list:
    for pageElement in page:
        if isinstance(pageElement, LTTextContainer):
            parse_element("TextContainer", pageNumber, pageElement, data)
            for text_line in pageElement:
                if not isinstance(text_line, LTAnno):
                    parse_element("TextLine", pageNumber, text_line, data)
                if len(contextMap) == 0:
                    return

def parse_pdf(filePath: str, data: dict) -> list:
    pageNumber = 0
    for page_layout in extract_pages(filePath):
        parse_page(page_layout, pageNumber, data)
        pageNumber += 1
        if len(contextMap) == 0:
            return

if "chargesByLineSummary" in dataDict and "currentY" in dataDict["chargesByLineSummary"]:
    del dataDict["chargesByLineSummary"]["currentY"]

parse_pdf(sys.argv[1], dataDict)

print(json.dumps(dataDict, indent=2))