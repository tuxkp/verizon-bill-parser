import json
import sys
from mypdfutils import MyPDFUtils

if len(sys.argv) < 2:
  print('Usage: vzw.py <MyBill_MM.DD.YYYY.pdf>')
  exit(1)

utils = MyPDFUtils(sys.argv[1])
print(json.dumps(utils.parsedData, indent=2))