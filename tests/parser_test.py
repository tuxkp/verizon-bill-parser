import pytest
from verizon_bill_parser import parser

def test_parser():
    dir_list = parser.parse_directory("data")
    assert dir_list == [("Vaishu Verizon Bill - Nov 27.pdf", 348784)]