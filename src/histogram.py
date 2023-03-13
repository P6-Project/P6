import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd


def createAllGraphs(inputFile: str, outputDir: str):
    dfs = createDfs(inputFile)

    absPath = os.path.abspath(outputDir)
    if not os.path.exists(absPath):
        os.mkdir(absPath)

    for df in dfs:
        fileName = df["Machine"].iloc[0]
        canDict = createDictCanPkl(df)
        diagram = createBarDiagramCanIds(canDict, fileName)
        diagram.savefig(os.path.join(absPath, fileName + ".png"), format="png")


def createBarDiagramCanIds(canIdDict: dict, fileName: str):
    plt.clf()
    plt.figure().set_figwidth(5 + (len(canIdDict) / 10))
    plt.bar(canIdDict.keys(), canIdDict.values(), 0.5)
    plt.xticks(rotation="vertical")
    plt.title(fileName)
    plt.xlabel("CAN Id")
    plt.ylabel("Quantity")
    plt.margins(0.01)
    plt.tight_layout()  # Else it cuts half of the bottom text.
    return plt


def createDfs(file) -> list[pd.DataFrame]:
    df: pd.DataFrame = pd.read_pickle(file)

    names = df["Machine"].unique()
    return [df[(df["Machine"] == name)] for name in names]


def createDictCanPkl(df: pd.DataFrame):
    can_id_dict = dict()

    for index, row in df.iterrows():
        if row["ID"] in can_id_dict:
            can_id_dict[row["ID"]] += 1
        else:
            can_id_dict[row["ID"]] = 1

    return can_id_dict


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("input")
    argparser.add_argument("output_folder")
    args = argparser.parse_args()

    createAllGraphs(args.input, args.output_folder)
