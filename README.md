# verizon-bill-parser
Script to parse a Verizon bill and extract the data into a JSON file.

Code is work in progress, does not work as of now.

## Installation
```
pip install -r requirements.txt
```

## Usage
```
python src/vzw.py <path to pdf>
```

## Output
```
{
    "bill_date": "2019-01-01",
    "bill_number": "123456789",
    "bill_period": "12/01/2018 - 12/31/2018",
    "bill_total": 123.45,
    "bill_usage": {
        "data": {
            "total": 123.45,
            "usage": [
                {
                    "amount": 123.45,
                    "date": "2018-12-01",
                    "type": "data"
                }
            ]
        },
        "messages": {
            "total": 123.45,
            "usage": [
                {
                    "amount": 123.45,
                    "date": "2018-12-01",
                    "type": "messages"
                }
            ]
        },
        "minutes": {
            "total": 123.45,
            "usage": [
                {
                    "amount": 123.45,
                    "date": "2018-12-01",
                    "type": "minutes"
                }
            ]
        }
    },
    "line_items": [
        {
            "amount": 123.45,
            "date": "2018-12-01",
            "description": "Line 1",
            "type": "line"
        },
        {
            "amount": 123.45,
            "date": "2018-12-01",
            "description": "Line 2",
            "type": "line"
        }
    ],
    "plan": {
        "data": {
            "amount": 123.45,
            "description": "Plan 1",
            "type": "plan"
        },
        "messages": {
            "amount": 123.45,
            "description": "Plan 2",
            "type": "plan"
        },
        "minutes": {
            "amount": 123.45,
            "description": "Plan 3",
            "type": "plan"
        }
    },
    "taxes": [
        {
            "amount": 123.45,
            "description": "Tax 1",
            "type": "tax"
        },
        {
            "amount": 123.45,
            "description": "Tax 2",
            "type": "tax"
        }
    ],
    "total": 123.45
}
```
