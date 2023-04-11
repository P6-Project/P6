import pytest
import pandas as pd
import os
from protocol_identifier.graph import id_histogram, id_pattern
from .helpers import FILES, DUMP

def test_id_histogram(tmp_path_factory):
    temp = tmp_path_factory.mktemp(DUMP)
    id_histogram(pd.read_pickle(FILES + "pkl/loxam.pkl"), temp / "loxam.png")
    assert os.path.exists(temp / "loxam.png")

def test_id_pattern(tmp_path_factory):
    temp = tmp_path_factory.mktemp(DUMP)
    id_pattern(pd.read_pickle(FILES + "pkl/loxam.pkl"), temp / "loxam.png")
    assert os.path.exists(temp / "loxam.png")
