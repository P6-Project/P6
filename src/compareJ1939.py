import argparse
import pickle

import pandas as pd


def loadKnownIDs(filePath: str) -> pd.DataFrame:
    with open(filePath, "r") as f:
        knownIDs: pd.DataFrame = pd.read_csv(f)
        return knownIDs


def importPickledData(filePath: str) -> pd.DataFrame:
    with open(filePath, "rb") as f:
        compareData: pd.DataFrame = pickle.load(f)
        return compareData


def compareKnownIDs(knownIDs: list, compareData: pd.DataFrame) -> list:
    j1939Machines: list = []
    for key in compareData["Machine"].unique():
        matches = pd.merge(
            knownIDs,
            compareData[compareData["Machine"] == key],
            left_on="ID_HEX",
            right_on="ID",
            how="inner",
        )
        num_matches = len(matches)
        # 1.2 is not set in stone, but it holds for the current data
        if (
            len(compareData[compareData["Machine"] == key])
            / (len(compareData[compareData["Machine"] == key]) - num_matches)
            > 1.2
        ):
            j1939Machines.append(key)
        print(f"{key} has {num_matches} matches")
    return j1939Machines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="compareJ1939", description="Compares known J1939 IDs to loxam data"
    )

    parser.add_argument("knownIDs")
    parser.add_argument("compareData")
    args = parser.parse_args()

    knownIDs = loadKnownIDs(args.knownIDs)
    compareData = importPickledData(args.compareData)
    j1939vehicles: list = compareKnownIDs(knownIDs, compareData)
    print(j1939vehicles)
