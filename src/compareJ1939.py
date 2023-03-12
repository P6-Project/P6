#Should load known CANBUS ID's from a file and compare them to the data in the pickle file
#Doing only one machine at the time, if there's a match of more than 5 ID's, then it's a match
#Else it's not a match

import pickle
import csv
import pandas as pd

def loadKnownIDs():
    with open(r"./knownPGN.csv", "r") as f:
        reader = csv.reader(f)
        knownIDs = list(reader)
        return knownIDs
    
def importPickledData():
    with open (r"./src/loxam.pkl", "rb") as f:
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
    knownIDs = loadKnownIDs()
    loxamData = importPickledData()
    compareKnownIDs(knownIDs, loxamData)
    print(loxamData.keys())