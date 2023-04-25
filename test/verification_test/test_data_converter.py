import pandas as pd
import pytest

from protocol_identifier.verification.data_converter import convert_to_float, extract_resolution, extract_offset, convert_data

def test_convert_to_float_1024():
    assert convert_to_float("1/1024") == 0.0009765625

def test_convert_to_float_32768():
    assert convert_to_float("1/32768") == 0.000030517578125

def test_convert_to_float_16():
    assert convert_to_float("1/16") == 0.0625

def test_convert_to_float_16_false():
    assert convert_to_float("1/16") != 0.062


def test_extract_resolution_simple_slash():
    assert extract_resolution("0.001/bit") == 0.001

def test_extract_resolution_simple_per():
    assert extract_resolution("0.5 rpm per bit") == 0.5

def test_extract_resolution_per_and_slash():
    assert extract_resolution("0.05 kg/h per bit") == 0.05

def test_extract_resolution_fraction():
    assert extract_resolution("1/1024 kg/s per bit") == 0.0009765625

def test_extract_resolution_fraction_without_per():
    assert extract_resolution("1/128 deg/bit") == 0.0078125

def test_extract_resolution_with_multiplier():
    assert extract_resolution("128 deg/7 bit") == 18.285714285714286

def test_extract_resolution_with_number_in_unit():
    assert extract_resolution("0.0125 mg/m3 per bit") == 0.0125


def test_extract_offset_simple_1():
    assert extract_offset("-1") == -1

def test_extract_offset_with_unit():
    assert extract_offset("-32127 rpm") == -32127


def test_convert_data_ASCII_unit():
    assert convert_data('0110', "1 / bit", "0", "ASCII") == 6

def test_convert_data_rpm_data():
    assert convert_data('1001101101000', "0.125 RPM per bit", "0", "rpm") == 621

def test_convert_data_voltage_current_data():
    assert convert_data('111111001010100', "0.05 A/bit", "-1600 A", "A") == 17
