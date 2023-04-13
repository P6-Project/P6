import pandas as pd

def get_data_range(data_range: str, units: str):
    try:
        if " to " in data_range:
            if units:
                data_range = data_range.split(units)[0].strip()
            low, high = data_range.split(" to ")
            high = high.split(" ")[0]
            return {
                "min" : float(low.replace(",", "")),
                "max" : float(high.replace(",", "")),
            }
    except:
        print("The data range:", data_range , "could not be derived.")
        return None
    return None


def check_data_point(readable_data: str, data_range: str, units: str):
    range = get_data_range(data_range, units)

    if range is None:
        return False
    if range["min"] < float(readable_data.replace(",","")) < range["max"]:
        return True
    return False


def check_readable_data(data: pd.DataFrame, usedSpns):

    usable_data = pd.DataFrame(columns=["PGN", "SPN", ])
    for index, row in data.iterrows():
        spn_row = usedSpns.loc[usedSpns["SPN"] == row["SPN"]]
        if check_data_point(row["Readable Data"], spn_row["Data Range"], spn_row["Units"]):
            usable_data.loc[len(usable_data.index)] = [row["PGN"], row["SPN"]]

    usable_data.drop_duplicates(subset=["SPN"], inplace=True)
    usable_data.reset_index(inplace=True)
    return usable_data

def get_usable_data_info(machine_data: pd.DataFrame, usedSpns: pd.DataFrame):

    usable_data = check_readable_data(machine_data, usedSpns)
    usable_data.to_csv("filter", sep='\t')