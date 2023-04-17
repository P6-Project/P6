
def extract_resolution(resolution):
    extracted_resolution = []
    if resolution.__contains__("per"):
        extracted_resolution = resolution.split("per")
    elif resolution.__contains__("/"):
        extracted_resolution = resolution.split("/")
    else:
        return 0

    x = 1

    print(extracted_resolution)

    if any(char.isdigit() for char in extracted_resolution[1]):
        x = int(extracted_resolution[1].strip().split(" ")[0])

    print("x: ", x)

    print(extracted_resolution)

    return convert_to_float(extracted_resolution[0].split(" ")[0])/x


def extract_offset(offset):
    offset_number = offset.split(" ")[0]
    return float(offset_number.replace(",", ""))


def convert_data(data: str, resolution: str, offset: str, units: str):
    if units in {"ASCII", "bit"}:
        return int(data, 2)
    converted_resolution = extract_resolution(resolution)
    converted_offset = 0
    if offset.strip() != "0":
        converted_offset = extract_offset(offset)

    print("Data: ", data)
    print("Converted resolution:", converted_resolution)
    print("Converted offset:", converted_offset)

    physical_value = int(data, 2) * converted_resolution + converted_offset

    return physical_value

def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac