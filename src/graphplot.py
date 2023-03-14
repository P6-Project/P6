import argparse

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle
import os

'''
This script takes the dataframe from loxam.pkl and creates graphs from all the datasets.
It also saves the datasets into a modelData.pkl file
'''


def createDataRow(subDataframe: pd.DataFrame, id: str, interval: int, amountRows: int):
    dataArray = []
    for x in range(amountRows):
        if id in subDataframe["ID"].array[x * interval:x * interval + interval]:
            dataArray.append(1)
        else:
            dataArray.append(0)
    return dataArray


def createDataMatrix(subDataframe: pd.DataFrame, uniqueIds: list, interval: int):
    matrix = []
    for id in uniqueIds:
        matrix.append(createDataRow(subDataframe, id, interval, int(len(subDataframe.index) / interval)))
    return matrix


def createModelData(dataframe: pd.DataFrame, interval: int, lenOfDataFrames: int, graphDir: str):
    arrayOfMatricies = []
    targets = []
    targetValue = 1
    for name in dataframe["Name"].unique():
        nameDataframe = dataframe.loc[dataframe["Name"] == name]
        listDataframe = [nameDataframe[i:i + lenOfDataFrames] for i in range(0, len(nameDataframe), lenOfDataFrames)]
        n = 1
        for subdataframe in listDataframe.__iter__():
            targets.append(targetValue)
            arrayOfMatricies.append(createDataMatrix(subdataframe, dataframe["ID"].unique(), interval))
            createGraph(subdataframe, graphDir + f'{subdataframe["Name"].iloc[0]} {n}')
            n += 1
        targetValue += 1
    return arrayOfMatricies, targets


def createGraph(subdataframe, dirname):
    # Apply the default theme
    sns.set_theme()

    # Putting a new figure on the stack
    plt.figure()

    # Plotting the dataframe
    sns_plot = sns.relplot(
        data=subdataframe,
        y="ID", x="Time", col="Action"
    )

    plt.savefig(dirname)
    plt.close()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog='Loxam Data Extractor',
        description='Converts to graphs and model data')

    argparser.add_argument("file")
    argparser.add_argument("outFolder")
    argparser.add_argument("outFile")
    args = argparser.parse_args()

    with open(args.file, "rb") as f:
        dataframe: pd.DataFrame = pickle.load(f)

    if not os.path.exists(args.outFolder):
        os.mkdir(args.outFolder)

    modelData = createModelData(dataframe, 10, 1000, args.outFolder)

    with open(args.outFile, "wb") as f:
        pickle.dump(modelData, f, protocol=pickle.HIGHEST_PROTOCOL)
