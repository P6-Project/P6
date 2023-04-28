import pytest
import pandas as pd
import pandas.testing as pdt

from protocol_identifier.protocol import parse_pgn, parse_data, parse_offset, parse_resolution, parse_data_range, parse_spn_length, parse_position, parse_byte_pos, byte_pos

# Test parse_pgn

def test_parse_pgn_dec():
    assert parse_pgn("0CF004FE") == 61444

def test_parse_pgn_with_hex_sign():
    assert parse_pgn("0x0CF004FE") == 61444

def test_parse_pgn_zero(): 
    assert parse_pgn("180000FE") == 0

def test_parse_pgn_low_number(): # Slicing a part of the string not existing.
    assert parse_pgn("180400FE") == 1024


# Test parse_data

def test_parse_data():
    assert parse_data("f06b93ac1d00f0ad") == "1010110111110000000000000001110110101100100100110110101111110000"


# Test parse_offset

def test_parse_offset_simple():
    assert parse_offset("-1") == -1.0

def test_parse_offset_with_unit():
    assert parse_offset("-32127 rpm") == -32127.0


# Test parse_resolution

def test_parse_resolution_simple_slash():
    assert parse_resolution("0.001/bit") == 0.001

def test_parse_resolution_kpa():
    assert parse_resolution("16 kPa/bit") == 16

def test_parse_resolution_simple_per():
    assert parse_resolution("0.5 rpm per bit") == 0.5

def test_parse_resolution_per_and_slash():
    assert parse_resolution("0.05 kg/h per bit") == 0.05

def test_parse_resolution_fraction():
    assert parse_resolution("1/1024 kg/s per bit") == 0.0009765625

def test_parse_resolution_fraction_without_per():
    assert parse_resolution("1/128 deg/bit") == 0.0078125

def test_parse_resolution_with_multiplier():
    assert parse_resolution("128 deg/7 bit") == 18.285714285714286

def test_parse_resolution_with_number_in_unit():
    assert parse_resolution("0.0125 mg/m3 per bit") == 0.0125


# Test parse_data_range

def test_parse_data_range_rpm_pgn_61444():
    assert parse_data_range("0 to 8,031.875 rpm") == (0, 8031.875)

def test_parse_data_range_negative_number():
    assert parse_data_range("-125 to 125 %") == (-125.0, 125)

def test_parse_data_range_wrong():
    assert parse_data_range(" ") == (0.0, 0.0)


# Test parse_spn_length

def test_parse_spn_length_byte():
    assert parse_spn_length("1 byte") == 8

def test_parse_spn_length_bytes():
    assert parse_spn_length("2 bytes") == 16

def test_parse_spn_length_bit():
    assert parse_spn_length("4 bits") == 4

def test_parse_spn_length_bit_and_byte():
    assert parse_spn_length("10 bits") == 10


# Test parse_position

def test_parse_position_rpm_range():
    assert parse_position("4-5") == 24

def test_parse_position_single_byte():
    assert parse_position("2") == 8

def test_parse_position_bit():
    assert parse_position("1.5") == 4

def test_parse_position_bit_and_byte():
    assert parse_position("1.7-2") == 6


# Test parse_byte_pos

def test_parse_byte_pos():
    assert parse_byte_pos("4") == 24

def test_parse_byte_pos_single_byte():
    assert parse_byte_pos("2") == 8

def test_parse_byte_pos_bit():
    assert parse_byte_pos("1.5") == 4

def test_parse_byte_pos_bit_and_byte():
    assert parse_byte_pos("1.7") == 6

# Test byte_pos

def test_byte_pos():
    assert byte_pos(4) == 24

def test_byte_pos_single_byte():
    assert byte_pos(2) == 8

def test_byte_pos_bit():
    assert byte_pos(1, 4) == 4

def test_byte_pos_bit_and_byte():
    assert byte_pos(1, 6) == 6


