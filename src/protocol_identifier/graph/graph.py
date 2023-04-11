import seaborn as sns
from pandas import DataFrame
import matplotlib.pyplot as plt
import os

def id_histogram(df: DataFrame, savePath: str):
    sns.set_theme()
    sns.histplot(data=df, x="ID")
    plt.savefig(savePath, format=os.path.splitext(savePath)[1][1:])
    plt.close()

def id_pattern(df: DataFrame, savePath: str, maxIDCount: int=-1):
    head = len(df.index) if maxIDCount == -1 else maxIDCount
    sns.set_theme()
    sns.relplot(data=df.head(head), y="ID", x="Time")
    plt.savefig(savePath, format=os.path.splitext(savePath)[1][1:])
    plt.close()