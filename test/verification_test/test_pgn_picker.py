import pandas as pd
import pytest

from protocol_identifier.verification.pgn_picker import check_spn, from_id_to_pgn_dec


def test_from_id_to_pgn_dec():
    assert from_id_to_pgn_dec("0CF004FE") == 61444

def test_from_id_to_pgn_dec_with_hex_sign():
    assert from_id_to_pgn_dec("0X0CF004FE") == 61444


def test_check_spn_return_true():
    assert check_spn(pd.Series([8], index = ["PGN Data Length"])) == True

def test_check_spn_return_false():
    assert check_spn(pd.Series([9], index = ["PGN Data Length"])) == False

def test_check_spn_return_true_with_string_input():
    assert check_spn(pd.Series(["5"], index = ["PGN Data Length"])) == True
