import pickle
from datetime import datetime
import argparse
import re
import os
import math
import sqlite3
from database import createDatabase

def loadData(directory: str, classifier: str, loader):
    table = [[], [], [], []] # time, id, class
    for file in os.listdir(directory):
        if classifier not in file:
            continue
        path = os.path.join(directory, file)
        canTable = loader(path)
        for i in range(len(table)):
            table[i] = [*table[i], *canTable[i]]
    return table     
        
def loadCanBusTester2CSV(path: str):
    names = os.path.splitext(os.path.basename(path))[0].split(" ")
    action = names.pop(-1)
    machine = " ".join(names)
    timeCol = []
    idCol = []
    machineCol = []
    actionCol = []
    hexRe = re.compile(r"\b[0-9A-Fa-f]+\b")
    
    with open(path, "r", encoding="utf8") as f:
        lines = f.readlines()
        
    
    #time = 0
    for csvLine in lines:
        #if i % 1000 == 0: time = 0
        line = csvLine.split(";")
        if hexRe.fullmatch(line[4]) == None:
            continue
        timeCol.append(line[2][:-4] + line[2][-3:]) # remove last comma
        idCol.append(line[4])
        machineCol.append(machine)
        actionCol.append(action)
        
        #time += 1

    maxSet = math.floor(len(timeCol) / 1000) * 1000     
    table = [timeCol[:maxSet], idCol[:maxSet], machineCol[:maxSet], actionCol[:maxSet]]
    timesLen = len(table[0])
    if not all(len(l) == timesLen for l in table):
        raise Exception("Lengths of table columns do not match!")
    return table



if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
                prog = 'create CanData Database')

    argparser.add_argument("database")
    argparser.add_argument("directory")
    args = argparser.parse_args()
    
    if not os.path.exists(args.database):
        print("Creating database...")
        table = loadData(args.directory, "", loadCanBusTester2CSV)
        table.append(["Loxam" for i in range(len(table[0]))])
        createDatabase(table, args.database)
        
    con = sqlite3.connect(args.database)
    cur = con.cursor()
    res = cur.execute("SELECT COUNT(*) FROM Machines")
    rows = res.fetchall()
    print(rows)

