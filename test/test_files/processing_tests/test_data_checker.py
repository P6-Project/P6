from protocol_identifier.verification import get_data_range, check_data_point
import pandas as pd


ranges = ["0 to 6425.5 ohm", "", "0 to 3", "0 to 250 %"]
units = ["ohm", "V", "", "%"]
values = ["3342.2", "223", "5", "25"]


def test_get_data_range():
    df = pd.DataFrame(zip(ranges, units), columns=["Data Range", "Units"])

    expected = [{"min": 0, "max": 6425.5}, None, {"min": 0, "max": 3}, {"min": 0, "max": 250}]
    out = list()
    for index, row in df.iterrows():
        out.append(get_data_range(row["Data Range"], row["Units"]))
    print(out)
    assert out == expected

def test_data_point_checker():
    df = pd.DataFrame(zip(values, ranges, units), columns=["Readable Data", "Data Range", "Units"])

    expected = [True, False, False, True]
    out = list()
    for index, row in df.iterrows():
        out.append(check_data_point(row["Readable Data"], row["Data Range"], row["Units"]))

    assert out == expected