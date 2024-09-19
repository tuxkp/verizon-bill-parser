import pytest
from verizon_bill_parser import parser

def test_parser():
    dir_list = parser.parse_directory("data")
    assert dir_list == [("Vaishu Verizon Bill - Nov 27.pdf", 348784)]

def test_parser_fail_1():
    try:
        dir_list = parser.parse_directory("data1")
    except Exception as e:
        assert str(e) == "Directory does not exist"
    