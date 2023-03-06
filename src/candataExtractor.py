import pickle
import os
from pprint import pprint
import argparse
import re

def loadCanData(directory: str):
    hexRe = re.compile(r"\b[0-9A-Fa-f]+\b")
    classifiers = ["idle", "run", "ignition", "off"]
    data = dict()
    for file in os.listdir(directory):
        canData = {"id": [], "time":[]}
        with open(os.path.join(directory, file), "r", encoding="utf8") as f:
            for line in f.readlines():
                eId, time = readIDTime(line)
                if hexRe.fullmatch(eId) == None:
                    continue
                canData["id"].append(eId)
                canData["time"].append(time)
        name = os.path.splitext(file)[0].split(" ")
        classifier = name.pop(-1)
        name = " ".join(name)
        if name in data:
            data[name][classifier] = canData
        else:
            data[name] = {classifier: canData}
    return data
        
def readIDTime(csvline: str):
    line = csvline.split(";") 
    return line[4], line[2]

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
            prog = 'Mendeley Data Converter',
            description = 'Converts to dict[str, list[int]] in pickle format')

    argparser.add_argument("folder")
    argparser.add_argument("out")
    args = argparser.parse_args()

    with open(args.out, "wb") as f:
            pickle.dump(loadCanData(args.folder), f, protocol=pickle.HIGHEST_PROTOCOL)
            

