import pandas as pd
import pickle
import os


def importRowFromXls(path: str, sheetName: str):
    df: pd.DataFrame = pd.read_excel(path, sheet_name=sheetName, skiprows=3)
    return df

def pruneHex(hexValues: list):
    return [element[2:-2]  if len(element) > 4 else element for element in hexValues]

def importMachinesPkl(path: str):
    with open(path, "rb") as f:
        machines: pd.DataFrame = pickle.load(f)
        return machines

def castHextoInt(hexValues: list):
    return [int(element, 16) for element in hexValues]    

def compareKnownPGNs(pgn: pd.DataFrame, machines: pd.DataFrame):
    machines = pd.DataFrame(machines)
    compare : dict = {}
    print(machines)
    for machine in machines["Machine"].unique():
        compare[machine] = 0
        matches = pd.merge(
            pgn,
            machines[machines["Machine"] == machine],
            left_on="PGN",
            right_on="ID",
            how="inner",
        )
        for match in matches["Machine"]:
            compare[machine] += 1
        num_matches = len(matches)
        
    print(compare)    

def removeOx(hexValues : list):
    return[value[2:] if value.startswith("0x") else value for value in hexValues]


def pruneMachineIDHex(machines: pd.DataFrame):
    machines["ID"] = removeOx(machines["ID"])
    machines["ID"] = pruneHex(machines["ID"])
    machines["ID"] = castHextoInt(machines["ID"])
       
    return machines
        


if __name__ == "__main__":
    with open ("./pgn.pkl", "rb") as f:
        pgn : pd.DataFrame = pd.read_pickle(f)
        machine : pd.DataFrame = importMachinesPkl("./out.pkl")
        machine = pruneMachineIDHex(machine)
        compareKnownPGNs(pgn, machine)
    

    
        