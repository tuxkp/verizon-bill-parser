import pytest
from verizon_bill_parser import parser

def test_parser():
    parser.set_logger_level("DEBUG")
    dir_list = parser.parse_directory("data")
    assert dir_list.__len__() == 8

def test_parser_fail_1():
    dir = "data1"
    try:
        dir_list = parser.parse_directory(dir)
    except Exception as e:
        assert str(e) == f"Directory {dir} does not exist"
    