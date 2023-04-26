import pandas as pd
import re

class SPNCollection:
    def __init__(self) -> None:
        self.__collection: dict[int, set[int]] = dict()
        
    def add(self, pgn: int, spn: int):
        if pgn in self.__collection:
            self.__collection[pgn].add(spn)
        else:
            self.__collection[pgn] = {spn}
            
    def remove(self, pgn: int, spn: int):
        self.__collection[pgn].remove(spn)
        
    def to_dataframe(self):
        df_dict = {"PGN": [], "SPN": []}
        
        for pgn, spn_set in self.__collection.items():
            for spn in spn_set:
                df_dict["PGN"].append(pgn)
                df_dict["SPN"].append(spn)
        return pd.DataFrame(df_dict)
    
    def __str__(self):
        return str(self.__collection)
  
#region PGN SPN Matching  
def find_j1939_protocol_matches(protocol: pd.DataFrame, machine: pd.DataFrame):
    collection = SPNCollection()

    for i, row in machine.iterrows():
        pgn = parse_pgn(row["ID"])
        protocol_subset = protocol[protocol["PGN"] == pgn]
        if protocol_subset.empty:
            continue
        
        bin_data = parse_data(row["Data"])
        
        for i, p_row in protocol_subset.iterrows():
            start: int = p_row["SPN Position in PGN"]
            end: int = start + p_row["SPN Length"]
            min_val: float = p_row["Data Range"][0]
            max_val: float = p_row["Data Range"][1]
            if end > 64: continue
            
            raw_spn_data = bin_data[start:end]
            spn_data: int = int(raw_spn_data, 2) * p_row["Resolution"] + p_row["Offset"]
            if min_val <= spn_data <= max_val:
                collection.add(pgn, p_row["SPN"])
    return collection
        
def parse_pgn(id: str) -> int:
    return int(bin(int(id, 16))[4:-8], 2)

def parse_data(data: str):
    ba = bytearray.fromhex(data)
    ba.reverse()
    return bin(int(ba.hex(), 16))[2:].zfill(64)
#endregion

#region protocol parsing
def convert_j1939(df: pd.DataFrame):
    df = df[df["PGN Data Length"] == 8]
    
    df["Resolution"] = df["Resolution"].apply(parse_resolution)
    df["Offset"] = df["Offset"].apply(parse_offset)
    df["Data Range"] = df["Data Range"].apply(parse_data_range)
    df["SPN Length"] = df["SPN Length"].apply(parse_spn_length)
    df["SPN Position in PGN"] = df["SPN Position in PGN"].apply(parse_position)
    
    return df
    
def parse_offset(offset: str) -> float:
    return float(offset.split(" ")[0].replace(",", ""))

def parse_resolution(res: str):
    temp_res = res.split("per") if "per" in res else res.split("/")
    if len(temp_res) == 1:
        return 1.0
    
    temp_num = temp_res[0].split(" ")[0].split("/")
    if len(temp_num) == 1:
        numerator = float(temp_num[0])
    else:
        numerator = float(temp_num[0]) / float(temp_num[1])
    
    temp_denom = temp_res[1].split(" ")[0]
    if re.match(r"[0-9]+(\.[0-9]*)?", temp_denom) is not None:
        denominator = float(temp_denom)
    else:
        denominator = 1.0
    return numerator / denominator

def parse_data_range(data_range: str):
    temp_range = data_range.split(" to ")
    if len(temp_range) == 1:
        return (0.0, 0.0)
    
    temp_low = temp_range[0].replace(",", "")
    temp_high = temp_range[1].split(" ")[0].replace(",", "")

    low = float(temp_low) if temp_low != "" else 0.0
    high = float(temp_high) if temp_high != "" else 1.0
    return (low, high)
    
def parse_spn_length(spn_length: str):
    temp_len = spn_length.split(" ")
    length = float(temp_len[0])
    if "byte" in temp_len[1]:
        length *= 8
    return int(length)

def parse_position(spn_position: str): 
    # this implementation does not support the format of 1,1.1, because there is literally no documentation on what that means   
    # why give a range and not just the start when the SPN length is given? this is a question only god can answer.
    return parse_byte_pos(spn_position.split("-")[0])
    
def parse_byte_pos(pos: str):
    if "." in pos:
        return byte_pos(int(pos[0]), int(pos[2]))
    return byte_pos(int(pos))

def byte_pos(start_byte: int, pos_in_byte: int=8):
    return (start_byte * 8) - 8 +  pos_in_byte
#endregion
