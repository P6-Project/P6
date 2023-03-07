import pandas
import os
import pickle
import numpy 
import argparse

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def trainingData(dataDir: str):
    paths = dict()
    for car in listdir_nohidden(dataDir):
        paths[car] = []
        carDir = os.path.join(dataDir, car)
        for exp in listdir_nohidden(carDir):
            expDir = os.path.join(carDir, exp)
            if exp == "unified.csv":
                paths[car].append(expDir)
            else:
                paths[car].append(expDir + "/unified.csv")
    return paths

def convertTrainingData(cars: dict[str, list[str]]):
    carsData: dict = dict()
    for car, paths in cars.items():
        cname = car[4:]
        carsData[cname] = []
        print(f"Converting {cname}")
        for i, path in enumerate(paths):
            print(path)
            data = pandas.read_csv(path, low_memory=False)
            carsData[cname].append([])
            for pid in data["id"]:
                carsData[cname][i].append(int(pid, 16))
    return carsData

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
                    prog = 'Mendeley Data Converter',
                    description = 'Converts to dict[str, list[int]] in pickle format')

    argparser.add_argument("folder")
    argparser.add_argument("out")
    args = argparser.parse_args()

    cars = trainingData(args.folder)
    carsData = convertTrainingData(cars)
    with open(args.out, "wb") as f:
            pickle.dump(carsData, f, protocol=pickle.HIGHEST_PROTOCOL)


