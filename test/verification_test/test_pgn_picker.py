import pandas as pd
import pandas.testing as pdt
import pytest

from protocol_identifier.verification.pgn_picker import check_spn, from_id_to_pgn_dec, prune_data, lookup_spns, match_pgns, read_j1939_file, read_loxam_machine_data


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


def test_prune_data():
    data = {
        "Data": ["f06b93ac1d00f0ad"],
        "BE Data": [""],
        "BE Bit Val": [""]
    }

    expected = {
        "Data": ["f06b93ac1d00f0ad"],
        "BE Data": ["adf0001dac936bf0"],
        "BE Bit Val": ["1010110111110000000000000001110110101100100100110110101111110000"]
    }

    df_in = pd.DataFrame(data)
    df_expected = pd.DataFrame(expected)

    pdt.assert_frame_equal(prune_data(df_in), df_expected)

# Something in the tests below are wrong.... 

# def test_match_pgns():
#     J1939_df = read_j1939_file("../J1939DA_201802.xls") # Should not be hardcoded...
#     data = read_loxam_machine_data("../test_machine.csv")
    
#     # data = {
#     # "ID": ["18FEDF00", "CF00A00", "CF00400", "18FF2C00"],
#     # "PGN": ["", "", "", ""],
#     # "Data": ["321", "222", "123", "333"]
#     # }

#     expected = {
#         "Can ID": ["18FEDF00", "CF00A00", "CF00400", "18FF2C00"],
#         "PGN": ["65247", "61450", "61444", "65324"],
#         "Data": ["321", "222", "123", "333"]
#     }

#     #df_in = pd.DataFrame(data)
#     df_expected = pd.DataFrame(expected)
#     result = match_pgns(data, J1939_df)

#     print(result)
#     print(df_expected)

#     pdt.assert_frame_equal(result, df_expected)


# def test_lookup_spns():
#     J1939_df = read_j1939_file("../J1939DA_201802.xls") # Should not be hardcoded...
#     #data = read_loxam_machine_data("../test_machine.csv")
    
#     data = {
#         "Can ID": ["18FEDF00", "CF00A00", "CF00400", "18FF2C00"],
#         "PGN": ["65247", "61450", "61444", "65324"],
#         "Data": ["4C000000583AFAFF", "4C000000583AFAFF", "4C000000583AFAFF", "4C000000583AFAFF"]
#     }

#     expected_machine = {
#         "Can ID": ["18FEDF00", "CF00A00", "CF00400", "18FF2C00"],
#         "PGN": ["65247", "61450", "61444", "65324"],
#         "Data": ["4C000000583AFAFF", "4C000000583AFAFF", "4C000000583AFAFF", "4C000000583AFAFF"]
#     }

#     df_in = pd.DataFrame(data)
#     df_machine_expected = pd.DataFrame(expected_machine)
#     machineData, usedSpns = lookup_spns(df_in, J1939_df)

#     print(df_machine_expected)
#     print(machineData)

#     pdt.assert_frame_equal(machineData, df_machine_expected)

