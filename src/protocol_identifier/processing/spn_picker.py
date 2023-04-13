import pandas as pd


def extract_data_range(range):
    try:
        data = [s.strip() for s in range.split(" to ")]
    except:
        print("No data range for this SPN")
    
    return []

def check_data(readable_data, range):
    data_range = extract_data_range(range)

    if readable_data >= data_range[0] or readable_data <= data_range[1]:
        return 1
    return 0


def find_usable_spns(machineDf: pd.DataFrame, spns: pd.DataFrame):
    for index, row in machineDf.iterrows():
        usedSpns = spns.loc[spns["PGN"] == row["PGN"]]

        readable_data = 1011 #Lasse insert data

        check_data(readable_data, row["Data Range"])