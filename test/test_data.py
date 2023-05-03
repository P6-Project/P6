import pytest
import shutil
import os
import pandas as pd
import pandas.testing as pdt

from protocol_identifier.data import load_loxam, load_csu, load_css, load_mendeley, load_renault
from protocol_identifier.data import extractor, converter
from protocol_identifier.data import load_pickled_dir, extract_pickled_dir
from protocol_identifier.data import list_files

from .helpers import helper_converter, assert_dict_df, FILES, DUMP


#region CSV Readers

def test_loxam_loader():
    expected = pd.read_pickle(FILES + "pkl/loxam.pkl")
    out = load_loxam(FILES + "csv/loxam.csv")
    pdt.assert_frame_equal(out, expected)

def test_csu_loader():
    expected = pd.read_pickle(FILES + "pkl/csu.pkl")
    out = load_csu(FILES + "csv/csu.csv")
    pdt.assert_frame_equal(out, expected)

def test_css_loader():
    expected = pd.read_pickle(FILES + "pkl/css.pkl")
    out = load_css(FILES + "csv/css.csv")
    pdt.assert_frame_equal(out, expected)

def test_mendeley_loader():
    expected = pd.read_pickle(FILES + "pkl/mendeley.pkl")
    out = load_mendeley(FILES + "csv/mendeley.csv")
    pdt.assert_frame_equal(out, expected)

def test_renault_loader():
    expected = pd.read_pickle(FILES + "pkl/renault.pkl")
    out = load_renault(FILES + "csv/renault.csv")
    pdt.assert_frame_equal(out, expected)

#endregion 

#region Extractor

def test_extractor():
    expected = {
        "loxam": pd.read_pickle(FILES + "pkl/loxam.pkl"),
        "renault": pd.read_pickle(FILES + "pkl/renault.pkl")
    }
    out = dict(extractor({
        FILES + "csv/loxam.csv": (load_loxam, False, []), FILES + "csv/renault.csv": (load_renault, False, [])
    }))

    assert_dict_df(expected, out)


def test_converter_pkl(tmp_path_factory):
    temp = tmp_path_factory.mktemp(DUMP)
    helper_converter(FILES, temp)
    expected = ["loxam.pkl", "renault.pkl"]
    out = os.listdir(temp)
    out.sort()
    assert out == expected

def test_converter_gz(tmp_path_factory):
    temp = tmp_path_factory.mktemp(DUMP)
    helper_converter(FILES, temp, True)
    expected = ["loxam.pkl.gz", "renault.pkl.gz"]
    out = sorted(os.listdir(temp))
    assert out == expected

#endregion

#region Pickle Reader

def test_load_pickled_dir(tmp_path_factory):
    temp = tmp_path_factory.mktemp(DUMP)
    helper_converter(FILES, temp)
    out = load_pickled_dir(temp)
    out = dict(sorted(out.items()))
    expected = {
        "loxam": pd.read_pickle(FILES + "pkl/loxam.pkl"),
        "renault": pd.read_pickle(FILES + "pkl/renault.pkl")
    }
    assert_dict_df(expected, out)

def test_extract_pickled_dir(tmp_path_factory):
    temp = tmp_path_factory.mktemp(DUMP)
    helper_converter(FILES, temp, True)
    extract_pickled_dir(temp)
    expected = ['loxam.pkl', 'loxam.pkl.gz', 'renault.pkl', 'renault.pkl.gz']
    out = sorted(os.listdir(temp))
    assert expected == out

#endregion
