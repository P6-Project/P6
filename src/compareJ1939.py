import pickle
import csv
import pandas as pd
import argparse


def loadKnownIDs(filePath: str):
    with open(filePath, "r") as f:
        knownIDs: pd.DataFrame = pd.read_csv(f)
        return knownIDs
    
def importPickledData(filePath: str):
    with open (filePath, "rb") as f:
        loxamData: pd.DataFrame = pickle.load(f)
        return loxamData
    
def figureOutKnownIDs(knownIDs: pd.DataFrame):
    print(knownIDs.keys())
    print(knownIDs['ID_HEX'])
    
def compareKnownIDs(knownIDs: list, loxamData: pd.DataFrame):
                   
    for key in loxamData["Name"].unique():
        matches = pd.merge(knownIDs, loxamData[loxamData["Name"] == key], left_on='ID_HEX', right_on='ID', how='inner')
        num_matches = len(matches)
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
    #figureOutKnownIDs(knownIDs)

    print(loxamData.keys())