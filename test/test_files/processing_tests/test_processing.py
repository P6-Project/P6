import pytest
import pandas as pd
from protocol_identifier.processing import norm_time, normalize_df, normalize_dfs
from test.helpers import FILES

def test_normalize_dfs():
    dfs = [
        pd.read_pickle(FILES + "pkl/loxam.pkl"),
        pd.read_pickle(FILES + "pkl/renault.pkl"),
        pd.read_pickle(FILES + "pkl/css.pkl")
    ]

    expected = [0, 1, 19, 20, 31, 0, 0, 1, 1, 5, 0, 1, 1, 3, 4]
    out = list(pd.concat(normalize_dfs(dfs, 5))["Time"])
    assert out == expected

def test_normalize_df():
    expected = [0, 1, 19, 20, 31]
    out = list(normalize_df(pd.read_pickle(FILES + "pkl/loxam.pkl"), 5)["Time"])
    assert out == expected


def test_norm_time():
    input = ["13:37:00.100000", "13:37:00.300000", "13:37:00.400000", "13:37:00.700000", "13:37:00.900000", "13:37:01.200000"]
    expected = [0, 200, 300, 0, 200, 500]
    out = norm_time(input, 3)
    assert out == expected
