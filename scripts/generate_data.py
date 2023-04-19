from random import randint, choices
import pandas as pd
import os

def create_data(num_lines : int) -> pd.DataFrame:
    temp: dict = {
        "ID": [],
        "Label": [],
    }
    weighted_ranges = [(0, 2**11 - 1), (2**11, 2**29)]
    weights = [0.2, 0.8]
    chosen_range = choices(weighted_ranges, weights)[0]
    for i in range(num_lines):
        
        temp["ID"].append(hex(randint(*chosen_range)))
        temp["Label"].append("Other")
    return pd.DataFrame(temp)

if __name__ == "__main__":
    if os.path.exists("../data/dfs/rand_data_noise.pkl.gz"):
        num_lines = 25000000
        # for files in os.listdir("../data/dfs"):
        #     if files.find("timeNormalized") != -1:
        #         df : pd.DataFrame =  pd.read_pickle(os.path.join("../data/dfs", files))
        #         num_lines += len(df)
        #         print(num_lines)
        df = create_data(num_lines)
        df.to_pickle("../data/dfs/rand_data_noise.pkl.gz")
    df = pd.read_pickle("../data/dfs/rand_data_noise.pkl.gz")
    print(df.head(100000), "done")

