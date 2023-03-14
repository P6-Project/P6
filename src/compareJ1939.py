import argparse
import pickle

import pandas as pd


def loadKnownIDs(filePath: str):
    with open(filePath, "r") as f:
        knownIDs: pd.DataFrame = pd.read_csv(f)
        return knownIDs


def importPickledData(filePath: str):
    with open(filePath, "rb") as f:
        loxamData: pd.DataFrame = pickle.load(f)
        return loxamData


def compareKnownIDs(knownIDs: list, loxamData: pd.DataFrame) -> list:
    j1939Machines: list = []
    for key in loxamData["Name"].unique():
        matches = pd.merge(
            knownIDs,
            loxamData[loxamData["Name"] == key],
            left_on="ID_HEX",
            right_on="ID",
            how="inner",
        )
        num_matches = len(matches)
        #1.2 is not set in stone, but it holds for the current data
        if (
            len(loxamData[loxamData["Name"] == key])
            / (len(loxamData[loxamData["Name"] == key]) - num_matches)
            > 1.2
        ):
            j1939Machines.append(key)
        print(f"{key} has {num_matches} matches")
    return j1939Machines

 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="compareJ1939", description="Compares known J1939 IDs to loxam data"
    )

    parser.add_argument("folder1")
    parser.add_argument("folder2")
    args = parser.parse_args()

    knownIDs = loadKnownIDs(args.folder1)
    loxamData = importPickledData(args.folder2)
    compareKnownIDs(knownIDs, loxamData)
