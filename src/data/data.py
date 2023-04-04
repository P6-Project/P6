import numpy as np
import pandas as pd
import os
from datetime import timedelta
import csv
from processing import normalizeDF

known_other : list = ["Houlotte lift", "Case stor", "Weidemann Ehofftrek 1160"]
known_J1939 : list = ["CSS Electronics"]

def load_pklgz(root : str, delimiter : int = 1, filename: str = "") -> list:
    dfs : list = []
    for files in os.listdir(root):
        if(files.find("timeNormalized") != -1 and delimiter == 1):
            filepath = os.path.join(root, files)
            dfs.append(pd.read_pickle(filepath))
        elif(files.find("binaryMatrix") != -1 and delimiter == 0):
            filepath = os.path.join(root, files)
            dfs.append(pd.read_pickle(filepath))
        elif(files.find("binaryMatrix") == -1 and files.find("timeNormalized") == -1 and delimiter == 2):
            filepath = os.path.join(root, files)
            dfs.append(pd.read_pickle(filepath))
        elif(files.find(filename) != -1 and delimiter == 3):
            print("found file: " + files + "")
            filepath = os.path.join(root, files)
            dfs.append(pd.read_pickle(filepath))  
    return dfs

def main(runFlag: bool = True, source : str = "./data/dfs", delimiter : int = 1, filename: str = ""):
    try:
        df = load_pklgz(source, delimiter, filename)
    except FileNotFoundError:
        print("No DF found matching the criteria")
        return None
    print("all dfs loaded")
    for d in df:
        if(runFlag == False):
            print(d.head(10))
            normalize_time(d)
            pd.to_pickle(d, "./data/dfs/" + d["Machine"].unique()[0] + " timeNormalized" + ".pkl.gz")
        make_binary_matrix(d)

def normalize_time(df):
    #if df["Time"].dtype == "float" convert to datetime:
    if df["Time"].dtype == float:
        df["Time"] = pd.to_datetime(df["Time"], unit="s")
    if df['Time'].dtype != 'datetime64[ns]':
        df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S.%f')
    print(df["Machine"].unique()[0] + " time normalized")
    try:
        df["Time"] = df["Time"].apply(lambda x: x - df["Time"].iloc[0])
        df["Time"] = df["Time"].apply(lambda x: x / timedelta(milliseconds=1))
    except TypeError as e:
        print(e)
        df["Time"] = df["Time"]
    print(df["Time"].head(10))

def add_label_to_binary_matrix(source : str, machine : str):
    labelDict : dict = {}
    for files in os.listdir(source):
        if(files.find(machine) != -1 and files.find("binaryMatrix") == -1):
            print("found machine file: " + files + "")
            df : pd.DataFrame = pd.read_pickle(source + files)
            if 'Source' in df and df['Source'].eq("CSS Electronics").all():
                a = df['Machine'].to_list()
                labelDict[a[0]] = "J1939"
            elif df["Machine"].isin(known_other).any():
                a = df['Machine'].to_list()
                labelDict[a[0]] = "Other"
            else:
                a = df['Machine'].to_list()
                labelDict[a[0]] = "Unknown"
        if(files.find("binaryMatrix") != -1 and files.find(machine) != -1):
            for keys in labelDict.keys():
                print("key: " + keys + " files: " + files)
                if files.find(keys) != -1:
                    df = pd.read_pickle("./data/dfs/" + files)
                    df["Label"] = labelDict[keys]
                    print(df.head(100))
                    pd.to_pickle(df, "./data/dfs/" + files)
    return df

def make_binary_matrix(df: pd.DataFrame, interval: int = 500) -> pd.DataFrame:
    # Create a new column with time intervals 
    bin_matrix : pd.DataFrame = pd.DataFrame()
    columns : list = [time for time in range(0, int(df["Time"].max()), interval)] 
    rows : list = [id for id in df["ID"].unique()]
    bin_matrix = pd.DataFrame(columns=columns, index=rows)
    i = 0
    for id in df["ID"].unique():
       id_df = df[df["ID"] == id]
       print("id_df: " + str(i) + " of " + str(len(df["ID"].unique())))
       i+=1
       for column in bin_matrix.columns:
           interval_df = id_df[(id_df["Time"] >= column) & (id_df["Time"] < column + interval)]
           if interval_df.empty:
               bin_matrix.loc[id, column] = 0
           else:
               bin_matrix.loc[id, column] = 1
    pd.to_pickle(bin_matrix, "./data/dfs/" + df["Machine"].unique()[0] + " binaryMatrix" + ".pkl.gz")
    print(bin_matrix.head(10))
            
def temp():
    dfs : list = []
    for dir in os.listdir("./data/data/"):
        if(dir.find("Online_car") != -1):
            for files in os.listdir("./data/data/" + dir + "/"):
                ##txt_to_csv("./data/data/" + dir + "/" + files, "./data/data/" + dir + "/" + files + ".csv")
                df = pd.read_csv("./data/data/" + dir + "/" + files, sep=",")
                pd.to_pickle(df, "./data/dfs/" + files + ".pkl.gz")
                dfs.append(df)
    return dfs

def txt_to_csv(file : str, output : str):
    with open(file, 'r') as infile, open(output, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Name', 'Time', 'ID', 'DLC', 'Data' ])
        for line in infile:
            parts = line.strip().split()
            name = file.split("/")[-1]
            timestamp = parts[1].rstrip('0').rstrip('.')
            identifier = parts[3]
            dlc = parts[6]
            data = parts[7:-1]
            writer.writerow([name, timestamp, identifier, dlc, data])
        
if __name__ == "__main__":
    #main(runFlag=False, source="./data/dfs/", delimiter=3, filename="normal_run")    
    add_label_to_binary_matrix(source="./data/dfs/", machine="normal_run")
    #temp()