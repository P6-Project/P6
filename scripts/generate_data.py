import pandas as pd
from random import randint, choices
import secrets
import os
import warnings
import numpy as np

# Suppress Pandas warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def can_data_generator(
    lines : int = 5000000, 
    with_data : bool = True, 
    location : str = "./data/dfs", 
    name : str = "rand_data_data", 
    file_ext : str = "pkl.gz"
    ) -> pd.DataFrame:
    """Generates random data for noise in model traning.
    can generate random data points such that it can be used
    in neural network training, with more datapoints"""
    columns = ["ID", "Data", "Label"] if with_data else ["ID", "Label"]

    ranges = np.array([(0, 2**11-1), (2**11, 2**29)], dtype=np.int64)
    weights = [0.2, 0.8]

    def generate_data():
        for i in range(lines):
            if(i % 100000 == 0):
                print(f"Generated {i} lines")
            id_string = randint(*choices(ranges, weights=weights)[0])
            if with_data:
                data_string = randint(0, 2**64-1)
                yield (id_string, data_string, "Unknown")
            else:
                yield (id_string, "Unknown")

    data = pd.DataFrame(generate_data(), columns=columns)
    data.to_pickle(os.path.join(location, name + "." + file_ext))

if __name__ == "__main__":
    can_data_generator()
    
    