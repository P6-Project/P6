
def extract_resolution(resolution: str):
    extracted_resolution = []
    if "per" in resolution:
        extracted_resolution = resolution.split("per")
    elif "/" in resolution:
        extracted_resolution = resolution.split("/")
    else:
        return 0

    x = 1
    if any(char.isdigit() for char in extracted_resolution[1]):
        x = int(extracted_resolution[1].strip().split(" ")[0]) # if the resolution says eg. 4 states / 2 bits

    return convert_to_float(extracted_resolution[0].split(" ")[0]) / x


def extract_offset(offset: str):
    offset_number = offset.split(" ")[0]
    return float(offset_number.replace(",", ""))


def convert_data(data: str, resolution: str, offset: str, units: str):
    if units in {"ASCII", "bit"}:
        return int(data, 2)
    converted_resolution = extract_resolution(resolution)
    converted_offset = 0
    if offset.strip() != "0":
        converted_offset = extract_offset(offset)

    physical_value = int(data, 2) * converted_resolution + converted_offset

    return physical_value

def convert_to_float(frac_str: str):
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