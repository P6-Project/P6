from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import pickle

'''
This script takes the dataframe from loxam.pkl and creates graphs from all the datasets.
It also saves the datasets into a data.pkl file
'''

def createDataRow(subDataframe, id):
    dataArray = []
    for x in range(100):
        if id in subDataframe["ID"].array[x * 10:x * 10 + 10]:
            dataArray.append(1)
        else:
            dataArray.append(0)
    return dataArray

def createDataMatrix(subDataframe, uniqueIds):
    matrix = []
    for id in uniqueIds:
        matrix.append(createDataRow(subDataframe, id))
    return matrix


def createModelData(dataframe):
    arrayOfMatricies = []
    targets = []
    targetValue = 1
    for name in dataframe["Name"].unique():
        nameDataframe = dataframe.loc[dataframe["Name"] == name]
        listDataframe = [nameDataframe[i:i + 1000] for i in range(0, len(nameDataframe), 1000)]
        n = 1
        for subdataframe in listDataframe.__iter__():
            targets.append(targetValue)
            arrayOfMatricies.append(createDataMatrix(subdataframe, dataframe["ID"].unique()))
            createGraph(subdataframe, f'{subdataframe["Name"].iloc[0]} {n}')
            n += 1
        targetValue += 1
    return arrayOfMatricies,targets

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


with open("./loxam.pkl", "rb") as f:
    dataframe: pd.DataFrame = pickle.load(f)

modelData = createModelData(dataframe)

with open("data.pkl", "wb") as f:
    pickle.dump(modelData, f, protocol=pickle.HIGHEST_PROTOCOL)