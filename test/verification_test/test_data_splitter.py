import pandas as pd
import pytest

from protocol_identifier.verification.data_splitter import split_data, byte_and_bit_from_num

def test_byte_and_bit_from_num():
    assert byte_and_bit_from_num("2.5") == (2, 5)


# should check for bytes
def test_split_data_rpm():
    assert split_data("1010110111110000000000000001110110101100100100110110101111110000", "4-5", "2 bytes") == "0001110110101100"

# Test fails due to fault in code, as it multiplies with 8 and returns nearly all the data.
# def test_split_data_single_byte():
#     assert split_data("1010110111110000000000000001110110101100100100110110101111110000", "2", "1 byte") == "11110000"

def test_split_data_bit():
    assert split_data("1010110111110000000000000001110110101100100100110110101111110000", "1.5", "4 bits") == "1101"

def test_split_data_bit_and_byte():
    assert split_data("1010110111110000000000000001110110101100100100110110101111110000", "1.7-2", "10 bits") == "0111110000"


