from random import randint, choices
import pandas as pd
import os

def create_data(num_lines : int, source : str) -> pd.DataFrame:
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

def main(source : str, num_lines : int):
    if not os.path.exists(source):
        os.makedirs(source)
    num_lines = 25000000
    df = create_data(num_lines, source)
    df.to_pickle("../data/dfs/rand_data_noise.pkl.gz")
    df = pd.read_pickle("../data/dfs/rand_data_noise.pkl.gz")
    print(df.head(100000), "done")

if __name__ == "__main__":
    main("../data/dfs/", 25000000)
