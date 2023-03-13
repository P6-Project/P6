from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import pickle

def create_row(dataframe, id):
    bitarray = []
    for x in range(100):
        if id in dataframe["ID"].array[x * 10:x * 10 + 10]:
            bitarray.append(1)
        else:
            bitarray.append(0)
    return bitarray

def create_matrix(dataset, unique_ids):
    matrix = []
    for id in unique_ids:
        matrix.append(create_row(dataset, id))
    return matrix

def create_graph(dataframe):
    array_of_matricies = []
    for x in dataframe["Name"].unique():
        x_dataframe = dataframe.loc[dataframe["Name"] == x]
        list_df = [x_dataframe[i:i + 1000] for i in range(0, len(x_dataframe), 1000)]
        n = 1
        for sublist in list_df.__iter__():
            array_of_matricies.append(create_matrix(sublist, dataframe["ID"].unique()))
            print_graph(sublist, f'{sublist["Name"].iloc[0]} {n}')
            n += 1
    return array_of_matricies

def print_graph(subdataframe, name):
    print(subdataframe)
    # Apply the default theme
    sns.set_theme()
    # Create a visualization
    plt.figure()
    sns_plot = sns.relplot(
        data=subdataframe,
        y="ID", x="Time" , col="Action"
    )
    plt.savefig(f'./graphs/{name}.png')
    plt.close()



with open("./loxam.pkl", "rb") as f:
    dataframe: pd.DataFrame = pickle.load(f)




print(len(dataframe["ID"].unique()))



file = create_graph(dataframe)



dataframe["ID"] = dataframe["ID"].apply(lambda x: int(x, 16))
target = dataframe["Name"]
dataframe = dataframe.drop("Name", axis=1).drop("Source", axis=1).drop("Action", axis=1)







