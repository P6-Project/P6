import pandas as pd

def get_data_range(data_range: str, units: str):
    print("DATA RANGE:", data_range, "Units:", units)
    try:
        if data_range.__contains__("to"):
            print("here1", units)
            if units or units == "0":
                data_range = data_range.split(units)[0].strip()
            low, high = data_range.split(" to ")
            high = high.split(" ")[0]
            return {
                "min" : float(low.replace(",", "")),
                "max" : float(high.replace(",", "")),
            }
    except:
        print("The data range:", data_range, "could not be derived.")
        return None
    return None


def check_data_point(readable_data: str, data_range: str, units: str):
    range = get_data_range(data_range, units)

    if range is None:
        return False
    if range["min"] < float(readable_data) < range["max"]:
        return True
    return False


def check_readable_data(data: pd.DataFrame, usedSpns):


    for index, row in data.iterrows():
        spn_row = usedSpns.loc[usedSpns["SPN"] == row["SPN"]]




def get_usable_data_info(machine_data: pd.DataFrame, usedSpns: pd.DataFrame):

    usable_data = check_readable_data(machine_data, usedSpns)
    usable_data.to_csv("filter", sep='\t')