import pandas as pd
from .data_splitter import split_data
from .data_converter import convert_data
from .data_checker import check_data_point


def find_usable_spns(machineDf: pd.DataFrame, spns: pd.DataFrame):
    usable_data = pd.DataFrame(columns=["PGN", "SPN"])
    for index, row in machineDf.iterrows():
        used_spns = spns.loc[spns["PGN"] == row["PGN"]]

        print(used_spns)
        print(row)
        if used_spns.empty:
            continue

        for spn_index, spn_row in used_spns.iterrows():
            print("-------------------------------------------------------")
            print("SPN VALUE: ", spn_row["SPN"])
            splitted_data = split_data(row["BE Bit Val"], spn_row["SPN Position in PGN"], spn_row["SPN Length"])
            print("SPLITTED DATA:", splitted_data)
            converted_data = convert_data(splitted_data, spn_row["Resolution"], spn_row["Offset"], spn_row["Units"])
            print("CONVERTED DATA:", converted_data, spn_row["Units"])
            if check_data_point(converted_data, spn_row["Data Range"], spn_row["Units"]):
                usable_data.loc[len(usable_data.index)] = [spn_row["PGN"], spn_row["SPN"]]


    usable_data.drop_duplicates(subset=["SPN"], inplace=True)
    usable_data.reset_index(inplace=True)
    return usable_data