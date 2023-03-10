import re, os, math
from pandas import DataFrame

def loadLoxam(directory: str):
    timeCol = []
    idCol = []
    nameCol = []
    actionCol = []
    sourceCol = []

    for file in os.listdir(directory):
        newTimes, newIds = loadCanBusTester2CSV(os.path.join(directory, file))
        
        names = os.path.splitext(file)[0].split(" ")
        action = names.pop(-1)
        name = " ".join(names)
        
        timeCol = [*timeCol, *newTimes]
        idCol = [*idCol, *newIds]
        nameCol = [*nameCol, *[name for _ in range(len(newTimes))]]
        actionCol = [*actionCol, *[action for _ in range(len(newTimes))]]
        sourceCol = [*sourceCol, *["Loxam" for _ in range(len(newTimes))]]
    return DataFrame({"Time": timeCol, "ID": idCol, "Name": nameCol, "Action": actionCol, "Source": sourceCol})  

def loadLoxamFile(directory, file):
    timeCol = []
    idCol = []
    nameCol = []
    actionCol = []
    sourceCol = []

    newTimes, newIds = loadCanBusTester2CSV(os.path.join(directory, file))
    
    names = os.path.splitext(file)[0].split(" ")
    action = names.pop(-1)
    name = " ".join(names)
    
    timeCol = [*timeCol, *newTimes]
    idCol = [*idCol, *newIds]
    nameCol = [*nameCol, *[name for _ in range(len(newTimes))]]
    actionCol = [*actionCol, *[action for _ in range(len(newTimes))]]
    sourceCol = [*sourceCol, *["Loxam" for _ in range(len(newTimes))]]
    return DataFrame({"Time": timeCol, "ID": idCol, "Name": nameCol, "Action": actionCol, "Source": sourceCol})  

def loadCanBusTester2CSV(path: str):
    idCol = []
    hexRe = re.compile(r"\b[0-9A-Fa-f]+\b")
    
    with open(path, "r", encoding="utf8") as f:
        lines = f.readlines()
    
    for csvLine in lines:
        line = csvLine.split(";")
        if hexRe.fullmatch(line[4]) == None:
            continue
        idCol.append(line[4])

    maxSet = math.floor(len(idCol) / 1000) * 1000     
    idCol = idCol[:maxSet]
    
    timeCol = []
    time = 0
    for i in range(maxSet):
        if i % 1000 == 0: time = 0
        timeCol.append(time)
        time += 1

    return timeCol, idCol
