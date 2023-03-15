import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def createAllGraphs(inputFile: str, outputDir: str):
    dfs = createDfs(inputFile)

    absPath = os.path.abspath(outputDir)
    if not os.path.exists(absPath):
        os.mkdir(absPath)   

    for df in dfs:
        fileName = df['Machine'].iloc[0] + " " + df['Action'].iloc[0]
        diagram = createBarDiagramCanIds(createDictCanPkl(df), fileName)
        diagram.savefig(os.path.join(absPath,fileName + ".png"), format="png") # high resulution pics: add "dpi=1200" (slow).

def createBarDiagramCanIds(canIdDict: dict, fileName: str):
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

def createDfs(file) -> list[pd.DataFrame]:
    df:pd.DataFrame = pd.read_pickle(file)
    dfs = list()

    names = df["Machine"].unique()
    df_machines:pd.DataFrame = [df[(df["Machine"] == name)] for name in names]

    for index, machine in enumerate(df_machines):
        actions = machine["Action"].unique()
        for action in actions:
            dfs.append(machine[(machine["Action"] == action)])
            
    return dfs

def createDictCanPkl(df: pd.DataFrame) -> dict():
    can_id_dict = dict()

    for index, row in df.iterrows():
        if row['ID'] in can_id_dict:
            can_id_dict[row['ID']] += 1
        else:
            can_id_dict[row['ID']] = 1

    return can_id_dict

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog = "Histograms over different vehicle readings",
        description = "Create histograms for each vehicle readings from a pickle format")

    argparser.add_argument("input", help = "Input file containing data in a pickle format.")
    argparser.add_argument("output_folder", help = "Directory to output graphs.")
    args = argparser.parse_args()

    createAllGraphs(args.input, args.output_folder)
