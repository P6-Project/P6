import argparse
import pandas as pd
from data.data import readCSVGeneral, generatePickledData, importPickledData


def compareKnownIDs(knownIDs: pd.DataFrame, loxamData: pd.DataFrame, set_flag: int) -> list:
    if(set_flag == 1):
        indexKey = "ID_HEX"
    else:
        indexKey = "ID"
    j1939Machines: list = []
    compare: dict = {}
    for id in knownIDs[indexKey].unique():
        compare[id] = [0, {}]
    for machine in loxamData["Machine"].unique():
        matches = pd.merge(
            knownIDs,
            loxamData[loxamData["Machine"] == machine],
            left_on=indexKey,
            right_on="ID",
            how="inner",
        )
        for match in matches[indexKey]:
            compare[match][0] += 1
            if machine not in compare[match][1]:
                compare[match][1][machine] = 0
            compare[match][1][machine] += 1
        num_matches = len(matches)
        # 1.2 is not set in stone, but it holds for the current data
        try:
            if (
                len(loxamData[loxamData["Machine"] == machine])
                / (len(loxamData[loxamData["Machine"] == machine]) - num_matches)
                > 1.2

            ):
                j1939Machines.append(machine)
        except ZeroDivisionError:
            pass

    for key in compare:
        if compare[key][0] != 0:
            print(f"{key} has {compare[key]} matches")

    return j1939Machines


def delimitData(loxamData: pd.DataFrame, identifiedMachines: list) -> list:
    knownIDs : pd.Dataframe =  {"ID": []}
    knownIDs = pd.DataFrame(knownIDs)
    for key in loxamData["Machine"].unique():
        if key in identifiedMachines:
            loxamData = loxamData[loxamData["Machine"] != key]

    knownIDs["ID"] = loxamData["ID"].unique()
    return [knownIDs,loxamData]


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
    j1939 = compareKnownIDs(knownIDs, loxamData, 1)
    knownIDs = delimitData(loxamData, j1939)[0]
    loxamData = delimitData(loxamData, j1939)[1]
    openCanish = compareKnownIDs(knownIDs, loxamData, 0)
    print(openCanish)
