import pytest
from protocol_identifier.normalize import norm_time

def test_norm_time():
    input = ["13:37:00.100000", "13:37:00.300000", "13:37:00.400000", "13:37:00.700000", "13:37:00.900000", "13:37:01.200000"]
    expected = [0, 200, 300, 0, 200, 500]
    out = norm_time(input, 3)
    assert out == expected
