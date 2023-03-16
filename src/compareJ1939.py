import argparse
import pickle

import pandas as pd
from data.data import readCSVGeneral, generatePickledData, importPickledData


def compareKnownIDs(knownIDs: list, loxamData: pd.DataFrame) -> list:
    j1939Machines: list = []
    for key in loxamData["Machine"].unique():
        matches = pd.merge(
            knownIDs,
            loxamData[loxamData["Machine"] == key],
            left_on="ID_HEX",
            right_on="ID",
            how="inner",
        )
        num_matches = len(matches)
        # 1.2 is not set in stone, but it holds for the current data
        if (
            len(loxamData[loxamData["Machine"] == key])
            / (len(loxamData[loxamData["Machine"] == key]) - num_matches)
            > 1.2
        ):
            j1939Machines.append(key)
        print(f"{key} has {num_matches} matches")
    return j1939Machines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="compareJ1939", description="Compares known J1939 IDs to loxam data",
    )

    parser.add_argument("KnownIDs", help="Path to known J1939 IDs")
    parser.add_argument("loxamData", help="Path to loxam data")
    args = parser.parse_args()

    if args.KnownIDs is None or args.loxamData is None:
        parser.print_help()
        exit(1)
    elif args.KnownIDs.endswith(".csv"):
        knownIDs = readCSVGeneral(args.KnownIDs, ["ID_HEX"])
        generatePickledData(knownIDs, "knownIDs")
        knownIDs = importPickledData("./knownIDs.pkl")
    else:
        knownIDs = importPickledData(args.KnownIDs)


    loxamData = importPickledData(args.loxamData)
    compareKnownIDs(knownIDs, loxamData)
