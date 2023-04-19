import pandas as pd

def find_used_spns(j1939_path: str, machine_data: pd.DataFrame):

    # machine_data er på formen: ID | Data
    j1939_df = read_j1939_file(j1939_path)

    usable_machine_data = match_pgns(machine_data, j1939_df)

    (machineData, usedSpns) = lookup_spns(usable_machine_data, j1939_df)

    return prune_data(machineData), usedSpns


def read_j1939_file(path: str):
    df = pd.read_excel(path, skiprows=3, sheet_name="SPNs & PGNs",
                       usecols=["PGN", "Parameter Group Label", "PGN Data Length", "SPN Position in PGN", "SPN",
                                "SPN Name", "SPN Length", "Resolution", "Offset", "Data Range", "Units"]).dropna(axis=0,
                                                                                                        subset=["PGN",
                                                                                                                "SPN"])
    df["PGN"] = df["PGN"].apply(int)
    df["SPN"] = df["SPN"].apply(int)
    return df


def read_loxam_machine_data(path: str):
    df = pd.read_csv(path, delimiter=";", skiprows=1, usecols=["Unnamed: 4", "1.Byte", "2.Byte", "3.Byte",
                                                               "4.Byte", "5.Byte", "6.Byte", "7.Byte", "8.Byte"])

    df = df.iloc[1:]
    df = df[:-1]
    df = df.rename(columns={"Unnamed: 4": "ID", "1.Byte": "1", "2.Byte": "2", "3.Byte": "3", "4.Byte": "4",
                            "5.Byte": "5", "6.Byte": "6", "7.Byte": "7", "8.Byte": "8"})

    for x in range(8):
        df[f'{x + 1}'].fillna('00', inplace=True)
        df[f'{x + 1}'] = df[f'{x + 1}'].apply(lambda n: str(n).zfill(2))

    df["Data"] = df["1"] + df["2"] + df["3"] + df["4"] + df["5"] + df["6"] + df["7"] + df["8"]

    df.drop(columns=["1", "2", "3", "4", "5", "6", "7", "8"], axis=1, inplace=True)

    return df


def from_id_to_pgn_dec(id: str) -> object:
    try:
        return int(bin(int(id, 16))[4:-8], 2)
    except ValueError:
        return 'Not Valid'


def binary_search(arr, low, high, x):
    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        return -1


def match_pgns(machine_df: pd.DataFrame, j1939: pd.DataFrame):
    new_df = pd.DataFrame(columns=['CAN ID', 'PGN', 'Data'])
    pgn_list = j1939["PGN"].to_numpy()
    for index, data_row in machine_df.iterrows():
        pgn = from_id_to_pgn_dec(data_row["ID"])
        if pgn == 'Not Valid':
            continue
        result = binary_search(pgn_list, 0, len(pgn_list) - 1, pgn)
        if result != -1:
            new_df.loc[len(new_df)] = data_row
            new_df["PGN"].loc[len(new_df)] = pgn
            new_df.index = new_df.index + 1
    return new_df


def check_spn(spn: pd.Series):
    if int(spn["PGN Data Length"]) > 8:  # length is too big for this project
        return 0
    else:
        return 1


def lookup_spns(machine_df: pd.DataFrame, j1939_sheet: pd.DataFrame):
    usable_spns = pd.DataFrame()
    machine_df.reset_index(drop=True, inplace=True)
    for index, data_row in machine_df.iterrows():
        df: pd.DataFrame = j1939_sheet.loc[j1939_sheet["PGN"] == data_row[1]]
        usable_spns = pd.concat([usable_spns, df[~df["PGN Data Length"].isna()]]).drop_duplicates().reset_index(drop=True)
        if usable_spns.empty:
            machine_df.drop(index, axis='rows', inplace=True)
            continue
    for index, row in usable_spns.iterrows():
        if not check_spn(row):
            usable_spns.drop(index, axis=0)

    machine_df.dropna(how='all', inplace=True, axis='rows')
    machine_df.reset_index(drop=True, inplace=True)

    return (machine_df, usable_spns)


def prune_data(df: pd.DataFrame):
    bit_len = 64

    for index, row in df.iterrows():
        ba = bytearray.fromhex(str(row["Data"]))
        ba.reverse()
        df.loc[index, "BE Data"] = ba.hex()
        df.loc[index, "BE Bit Val"] = bin(int(df.loc[index, "BE Data"], 16))[2:].zfill(bit_len)
    return df
