import pickle
import csv
import pandas as pd
import argparse


def loadKnownIDs(filePath: str):
    with open(filePath, "r") as f:
        reader = csv.reader(f)
        knownIDs = list(reader)
        return knownIDs
    
def importPickledData(filePath: str):
    with open (filePath, "rb") as f:
        loxamData: pd.DataFrame = pickle.load(f)
        return loxamData
    
def compareKnownIDs(knownIDs: list, loxamData: pd.DataFrame):
    for key in loxamData:
        knownIDs = knownIDs[0]
        subset = loxamData[key]
        for key2 in subset:
            subset2 = subset[key2]
            set1 = set(subset2['id'])
            set2 = set(knownIDs)
            num_matches = len(set1.intersection(set2))
            print(f"{key} has {num_matches} matches")

    
        
if __name__ == "__main__":
    print("Enter the path to the known J1939 IDs file, and the path to the pickled data file")
    parser = argparse.ArgumentParser(
        prog = 'compareJ1939',
        description = 'Compares known J1939 IDs to loxam data')
    
    parser.add_argument("folder1")
    parser.add_argument("folder2")
    args = parser.parse_args()

    knownIDs = loadKnownIDs(args.folder1)
    loxamData = importPickledData(args.folder2)
    compareKnownIDs(knownIDs, loxamData)

    print(loxamData.keys())