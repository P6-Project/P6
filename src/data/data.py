import pandas as pd
import os
from datetime import timedelta

known_other : list = ["Houlotte lift", "Case stor", "Weidemann Ehofftrek 1160"]
known_J1939 : list = ["CSS Electronics"]

def load_pklgz(root : str, delimiter : bool = True) -> list:
    dfs : list = []
    for files in os.listdir(root):
        if(files.find("binaryMatrix") != -1):
            filepath = os.path.join(root, files)
            dfs.append(pd.read_pickle(filepath))
    return dfs

def main(runFlag: bool = True):
    df = load_pklgz("./data/dfs")
    print("all dfs loaded")
    for d in df:
        if(runFlag == False):
            normalize_time(d)
            pd.to_pickle(d, "./data/dfs/" + d["Machine"].unique()[0] + " timeNormalized" + ".pkl.gz")
            make_binary_matrix(d)
                  
def add_label_to_binary_matrix():
    labelDict : dict = {}
    for files in os.listdir("./data/dfs"):
        if(files.find("binaryMatrix") == -1 and files.find("timeNormalized") == -1):
            df : pd.DataFrame = pd.read_pickle("./data/dfs/" + files)
            if df['Source'].eq("CSS Electronics").all():
                a = df['Machine'].to_list()
                labelDict[a[0]] = "J1939"
            elif df["Machine"].isin(known_other).any():
                a = df['Machine'].to_list()
                labelDict[a[0]] = "Other"
            else:
                a = df['Machine'].to_list()
                labelDict[a[0]] = "Unknown"
    for files in os.listdir("./data/dfs"):
        if(files.find("binaryMatrix") != -1 ):
            for keys in labelDict.keys():
                print("key: " + keys + " files: " + files)
                if files.find(keys) != -1:
                    df = pd.read_pickle("./data/dfs/" + files)
                    df["Label"] = labelDict[keys]
                    print(df.head(10))
                    pd.to_pickle(df, "./data/dfs/" + files)
    return df

def make_binary_matrix(df: pd.DataFrame, interval: int = 5000) -> pd.DataFrame:
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
    
        
if __name__ == "__main__":
    #print pwd
    print("pwd=" + os.getcwd())
    add_label_to_binary_matrix()
    main()    