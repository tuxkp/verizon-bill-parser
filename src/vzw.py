import json
import sys
from pdfminer.high_level import extract_text

if len(sys.argv) < 2:
  print('Usage: vzw.py <bill_name.pdf>')
  exit(1)

print(sys.argv[1])

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTAnno
pages = []
for page_layout in extract_pages(sys.argv[1]):
    elements = []
    for element in page_layout:
        lines = []
        if isinstance(element, LTTextContainer):
            for text_line in element:
                if not isinstance(text_line, LTAnno):
                    lines.append({
                        'height': text_line.height,
                        'text': text_line.get_text(),
                        'width': text_line.width
                    })
        elements.append({
            "type": "element",
            "lines": lines
        })

    pages.append({
        "type": "page",
        "elements": elements
    })
print(json.dumps(pages))