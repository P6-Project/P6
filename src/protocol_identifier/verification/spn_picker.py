import pandas as pd
from protocol_identifier.verification.data_splitter import split_data
from protocol_identifier.verification.data_converter import convert_data
from protocol_identifier.verification.data_checker import check_data_point


def find_usable_spns(machine_df: pd.DataFrame, spns: pd.DataFrame):
    usable_data = pd.DataFrame(columns=["PGN", "SPN"])
    for index, row in machine_df.iterrows():
        used_spns = spns.loc[spns["PGN"] == row["PGN"]]

        if used_spns.empty:
            continue

        for spn_index, spn_row in used_spns.iterrows():
            # Some spn length values does not follow the format data length and type ~50 instances.
            try:
                splitted_data = split_data(row["BE Bit Val"], spn_row["SPN Position in PGN"], spn_row["SPN Length"])
            except ValueError:
                continue
            converted_data = convert_data(splitted_data, spn_row["Resolution"], spn_row["Offset"], spn_row["Units"])
            if check_data_point(converted_data, spn_row["Data Range"], spn_row["Units"]):
                usable_data.loc[len(usable_data.index)] = [spn_row["PGN"], spn_row["SPN"]]


    usable_data.drop_duplicates(subset=["SPN"], inplace=True)
    usable_data.reset_index(inplace=True, drop=True)
    return usable_data
