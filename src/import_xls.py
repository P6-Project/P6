import pandas as pd
import pickle
import os


def importRowFromXls(path: str, sheetName: str):
    df: pd.DataFrame = pd.read_excel(path, sheet_name=sheetName, skiprows=3)
    return df

def pruneHex(hexValues: list):
    return [element[2:-2] for element in hexValues if len(element) > 4]

def importMachinesPkl(path: str):
    with open(path, "rb") as f:
        machines: pd.DataFrame = pickle.load(f)
        return machines

def castHextoInt(hexValues: list):
    return [int(element, 16) for element in hexValues]    

def compareKnownPGNs(pgn: pd.DataFrame, machines: pd.DataFrame):
    matches = {}
    machines = pd.DataFrame(machines)
    for machine in machines:
        matches[machine] = 0
        for elem in pgn:
            for action in machines[machine]:
                if not isinstance(action, float):
                    if elem in action["id"]:
                        matches[machine] += 1
    print(matches)

def pruneMachineIDHex(machines: pd.DataFrame):
    for key in machines:
        machines[key]["id"] = pruneHex(machines[key]["id"])
        machines[key]["id"] = castHextoInt(machines[key]["id"])
       # print(machines[key]["id"])
    return machines
        


if __name__ == "__main__":
    with open ("./pgn.pkl", "rb") as f:
        pgn : pd.DataFrame = pd.read_pickle(f)
        machine : pd.DataFrame = importMachinesPkl("./machines.pkl")
        for key in machine:
            key = pruneMachineIDHex(machine[key])
        compareKnownPGNs(pgn, machine)
    

    
        