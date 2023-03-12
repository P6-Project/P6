import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def createAllGraphs(inputFile, outputDir):
    dfs = createDfs(inputFile)

    for df in dfs:
        fileName = df['Name'].iloc[0]
        canDict = createDictCanPkl(df)
        diagram = createBarDiagramCanIds(canDict, fileName)
        diagram.savefig(os.path.join(outputDir,fileName, ".png"), format="png")

def createBarDiagramCanIds(canIdDict, fileName):
    plt.clf()
    plt.figure().set_figwidth(5 + (len(canIdDict)/10))
    plt.bar(canIdDict.keys(), canIdDict.values(), 0.5)
    plt.xticks(rotation='vertical')
    plt.title(fileName)
    plt.xlabel('CAN Id')
    plt.ylabel('Quantity')
    plt.margins(0.01)
    plt.tight_layout() # Else it cuts half of the bottom text.
    return plt

def createDfs(file):
    df:pd.DataFrame = pd.read_pickle(file)

    names = df["Name"].unique()
    return [df[(df["Name"] == name)] for name in names]

def createDictCanPkl(df):
    can_id_dict = dict()

    for index, row in df.iterrows():
        if row['ID'] in can_id_dict:
            can_id_dict[row['ID']] += 1
        else:
            can_id_dict[row['ID']] = 1

    return can_id_dict

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("input")
    argparser.add_argument("output_folder")
    args = argparser.parse_args()


    createAllGraphs(args.input, args.output_folder)
