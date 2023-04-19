def get_data_range(data_range: str, units: str):
    try:
        if "to" in data_range:
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