import pytest
import pandas as pd
import pandas.testing as pdt

from protocol_identifier.protocol import parse_pgn, parse_data, parse_offset

# Test parse_pgn

def test_parse_pgn_dec():
    assert parse_pgn("0CF004FE") == 61444

def test_parse_pgn_with_hex_sign():
    assert parse_pgn("0x0CF004FE") == 61444

###### Fails but is possible (part of J1939) 

# def test_parse_pgn_zero(): 
#     assert parse_pgn("0") == 0

# def test_parse_pgn_low_number(): # Slicing a part of the string not existing.
#     assert parse_pgn("400") == 1024

##################


# Test parse_data

def test_parse_data():
    assert parse_data("f06b93ac1d00f0ad") == "1010110111110000000000000001110110101100100100110110101111110000"


# Test parse_offset

def test_parse_offset_simple_1():
    assert parse_offset("-1") == -1.0

def test_parse_offset_with_unit():
    assert parse_offset("-32127 rpm") == -32127.0
