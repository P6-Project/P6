import pandas as pd
from typing import Callable
from .time_parser import loxam_date_parser, unix_time_parser, date_parser
import re

def load_loxam(path: str):
    return generic_csv(path, {
        "Time": (None, loxam_date_parser),
        "ID":   (4,    None),
        "Data": (None, lambda x: "".join(x[5:-1])),
    }, sep=";", skiprows=3, headersRegex={"ID": r"\b[0-9A-Fa-f]+\b"})

def load_csu(path: str):
    return generic_csv(path, {
        "Time": (0, unix_time_parser),
        "ID":   (2, lambda x: x.split("#")[0]),
        "Data": (2, lambda x: x.split("#")[1].replace("\n", ""))
    }, sep=" ")

def load_renault(path: str):
    return generic_csv(path, {
        "Time": (0,    date_parser),
        "ID":   (1,    lambda x: x[2:]),
        "Data": (None, lambda x: "".join(hex(int(d.replace("\n", "")))[2:].zfill(2) for d in x[2:-1]).upper())
    }, skiprows=1, headersRegex={"ID": r"\b0x[0-9A-Fa-f]+\b"}, sep=";")

def load_css(path: str):
    df = pd.read_csv(path, sep=";", usecols=["TimestampEpoch", "ID", "DataBytes"])
    df.columns = ["Time", "ID", "Data"]
    df["Time"] = df["Time"].apply(lambda x: unix_time_parser(str(x)))
    return df

def load_mendeley(path: str):
    return generic_csv(path, {
        "Time": (0, unix_time_parser),
        "ID":   (2, None),
        "Data": (4, lambda x: hex(int(x, 2))[2:])
    })

def generic_csv(path: str, headers: dict[str, tuple[int, Callable]], sep:str=",", skiprows: int=0, headersRegex: dict[str, str]=dict()):
    regex: dict = {k: re.compile(v) for k, v in headersRegex.items()}
    csv: dict = {k:[] for k in list(headers.keys())}
    with open(path, "r") as f:
        for line in f.readlines()[skiprows:]:
            row = line.split(sep)
            for key, (i, func) in headers.items():
                val = row[i] if i is not None else row
                if key in regex and regex[key].fullmatch(row[i]) is None:
                    continue
                csv[key].append(func(val) if func is not None else row[i])
    return pd.DataFrame(csv)
