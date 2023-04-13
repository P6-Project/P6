def splitData(bitValue: int, range: str, length: str):
    sections = [s.strip() for s in range.split(",")]
    if len(sections) > 1:
        if len(sections) > 2:
            print("Section length too big")

        if "." in sections[0]:
            byte, bit = byte_and_bit_from_num(sections[0])
            start = (int(byte) * 8 - 8) + int(bit) - 1
        else:
            start = (int(sections[0]) * 8 - 8)

        if "." in sections[1]:
            byte, bit = byte_and_bit_from_num(sections[1])
            end = (int(byte) * 8 - 8) + int(bit) - 1
        else:
            end = (int(sections[1]) * 8 - 8)

        return bitValue[start:end]

    section = sections[0]
    if "." in section:
        byte, bit = byte_and_bit_from_num(section)
        start = (int(byte) * 8 - 8) + int(bit) - 1
        end = start + (int(length) * 8)

def byte_and_bit_from_num(num):
    parts = num.split(".")
    byte = parts[0]
    bit = parts[1] if len(parts) > 1 else 1
    return int(byte), int(bit)