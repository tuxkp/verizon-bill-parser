import re
import json
import PyPDF2

def extract_verizon_bill_data(pdf_path):
    data = {}

    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Extract text from each page
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        # Extract relevant information using regular expressions
        data['account_number'] = re.search(r'Account Number: (\d+)', text).group(1)
        data['bill_date'] = re.search(r'Bill Date: (\d{2}/\d{2}/\d{4})', text).group(1)
        data['due_date'] = re.search(r'Due Date: (\d{2}/\d{2}/\d{4})', text).group(1)

        # Extract itemized charges
        charges = re.findall(r'(\d+)\s+(\d{2}/\d{2}/\d{2})\s+(.*)\s+(-?\d+\.\d{2})', text)
        data['charges'] = []
        for charge in charges:
            item = {
                'quantity': charge[0],
                'date': charge[1],
                'description': charge[2],
                'amount': charge[3]
            }
            data['charges'].append(item)

    return data

# Example usage
pdf_path = 'verizon_bill.pdf'
bill_data = extract_verizon_bill_data(pdf_path)

# Output the extracted data as JSON
json_data = json.dumps(bill_data, indent=4)
print(json_data)
