import pandas as pd
import pytest

from protocol_identifier.verification.data_checker import check_data_point, get_data_range


def test_get_data_range_rpm_pgn_61444():
    assert get_data_range("0 to 8,031.875 rpm", "rpm") == {'min': 0, 'max': 8031.875}

def test_get_data_range_negative_number():
    assert get_data_range("-125 to 125 %", "%") == {'min': -125, 'max': 125}

def test_get_data_range_missing_to_in_range():
    assert get_data_range("1", "bit") == None


def test_check_data_point_rpm():
    assert check_data_point("621", "0 to 8,031.875 rpm", "rpm") == True

def test_check_data_point_rpm_out_of_range_negative():
    assert check_data_point("-1", "0 to 8,031.875 rpm", "rpm") == False

def test_check_data_point_rpm_out_of_range():
    assert check_data_point("10000", "0 to 8,031.875 rpm", "rpm") == False

def test_check_data_point_None():
    assert check_data_point("12", "1", "bit") == False
    