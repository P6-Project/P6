import argparse
import pickle

import pandas as pd
from data.data import readCSVGeneral, generatePickledData, importPickledData


def compareKnownIDs(knownIDs: pd.DataFrame, loxamData: pd.DataFrame) -> list:
    j1939Machines: list = []
    compare: dict = {}
    for key in knownIDs["ID_HEX"].unique():
        compare[key] = [0, {}]
    for key in loxamData["Machine"].unique():
        matches = pd.merge(
            knownIDs,
            loxamData[loxamData["Machine"] == key],
            left_on="ID_HEX",
            right_on="ID",
            how="inner",
        )
        for match in matches["ID_HEX"]:
            compare[match][0] = compare[match][0] + 1
            if key not in compare[match][1]:
                compare[match][1][key] = 0
            compare[match][1][key] += 1
        num_matches = len(matches)
        # 1.2 is not set in stone, but it holds for the current data
        if (
            len(loxamData[loxamData["Machine"] == key])
            / (len(loxamData[loxamData["Machine"] == key]) - num_matches)
            > 1.2
        ):
            j1939Machines.append(key)

    for key in compare:
        if compare[key][0] != 0:
            print(f"{key} has {compare[key]} matches")

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
