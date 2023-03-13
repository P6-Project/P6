import os
import re

import pandas as pd

from .parser import (
    CSUDateParser,
    CSUIDParser,
    dateParser,
    loxamDateParser,
    renaultIDParser,
)

HEXRE = re.compile(r"\b[0-9A-Fa-f]+\b")


def readDirCanData(dirPath: str, nrows: int):
    dfs = []
    for directory in sorted(os.listdir(dirPath)):
        nextPath = os.path.join(dirPath, directory)
        for file in sorted(os.listdir(nextPath)):
            dfs.append(readCSVCanData(os.path.join(nextPath, file), nrows))
    return dfs


def readCSVCanData(path: str, nrows: int):
    dirname = os.path.basename(os.path.dirname(path))
    filename = os.path.basename(os.path.splitext(path)[0])
    df: pd.DataFrame = None

    if dirname == "CSU":
        df = pd.read_csv(path, sep=" ", usecols=[0, 2], nrows=nrows, header=None)
        df.iloc[:, 1] = df.iloc[:, 1].apply(CSUIDParser)
        df.iloc[:, 0] = df.iloc[:, 0].apply(CSUDateParser)
    elif dirname == "Loxam":
        df = readCSV(
            path, ";", nrows, 4, 2, loxamDateParser, r"\b[0-9A-Fa-f]+\b", extraTimepos=1
        )
    elif dirname == "Mendeley":
        df = pd.read_csv(path, sep=",", usecols=["time", "id"], nrows=nrows)
        df["time"] = df["time"].apply(dateParser)
    elif dirname == "Renault":
        df = readCSV(path, ";", nrows, 1, 0, dateParser, r"\b0x[0-9A-Fa-f]+\b")
        df.iloc[:, 1] = df.iloc[:, 1].apply(renaultIDParser)
    else:
        raise Exception(f"No CSV Reader for {dirname}")

    df.columns = ["Time", "ID"]

    names = filename.split(" ")
    action = names.pop(-1)
    machine = " ".join(names)
    rowCount = len(df.index)

    df["Machine"] = [machine] * rowCount
    df["Action"] = [action] * rowCount
    df["Source"] = [dirname] * rowCount
    df["Time"] = df["Time"].apply(str)
    return df


def readCSV(
    path: str,
    sep: str,
    nrows: int,
    idpos: int,
    timepos: int,
    dateParser,
    idMatch: str,
    extraTimepos: int = -1,
):
    hexRe = re.compile(idMatch)
    idCol = []
    tCol = []
    with open(path, "r") as f:
        lines = f.readlines()
        rcount = 0
        for l in lines:
            if rcount == nrows:
                break
            ls = l.split(sep)
            id = ls[idpos]
            if hexRe.fullmatch(id) == None:
                continue
            t = ls[timepos]
            if extraTimepos != -1:
                t = ls[extraTimepos] + " " + t
            tCol.append(dateParser(t))
            idCol.append(id)
            rcount += 1
    return pd.DataFrame({"Time": tCol, "ID": idCol})
