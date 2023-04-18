from random import randint
import pandas as pd
import os

def create_data(num_lines : int) -> pd.DataFrame:
    temp: dict = {
        "ID": [],
        "Label": [],
    }
    for i in range(num_lines):
        temp["ID"].append(randint(0, 2**29))
        temp["Label"].append("Other")
    return pd.DataFrame(temp)

if __name__ == "__main__":
    #df = create_data(50000000)
    #df.to_pickle("../data/dfs/rand_data_noise.pkl.gz")
    df = pd.read_pickle("../data/dfs/rand_data_noise.pkl.gz")
    print(df.head(100000), "done")

