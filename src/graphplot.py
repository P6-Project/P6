import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle

'''
This script takes the dataframe from loxam.pkl and creates graphs from all the datasets.
It also saves the datasets into a modelData.pkl file
'''

def createDataRow(subDataframe, id, interval, amountRows):
    dataArray = []
    for x in range(int(amountRows)):
        if id in subDataframe["ID"].array[x * interval:x * interval + interval]:
            dataArray.append(1)
        else:
            dataArray.append(0)
    return dataArray

def createDataMatrix(subDataframe, uniqueIds, interval):
    matrix = []
    for id in uniqueIds:
        matrix.append(createDataRow(subDataframe, id, interval, len(subDataframe.index)/interval))
    return matrix


def createModelData(dataframe, interval, lenOfDataFrames):
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
            createGraph(subdataframe, f'{subdataframe["Name"].iloc[0]} {n}')
            n += 1
        targetValue += 1
    return arrayOfMatricies, targets

def createGraph(subdataframe, filename):
    # Apply the default theme
    sns.set_theme()

    # Putting a new figure on the stack
    plt.figure()

    #Plotting the dataframe
    sns_plot = sns.relplot(
        data=subdataframe,
        y="ID", x="Time" , col="Action"
    )

    plt.savefig(f'./graphs/{filename}.png')
    plt.close()

if __name__ == "__main__":
    with open("./src/loxam.pkl", "rb") as f:
        dataframe: pd.DataFrame = pickle.load(f)

    modelData = createModelData(dataframe, 10, 1000)

    with open("./src/modelData.pkl", "wb") as f:
        pickle.dump(modelData, f, protocol=pickle.HIGHEST_PROTOCOL)