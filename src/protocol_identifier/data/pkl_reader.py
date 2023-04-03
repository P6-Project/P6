import os
import pandas as pd
from .utils import list_files

def load_pickled_dir(dir: str):
    dfs: dict[str, pd.DataFrame] = dict()
    for path in list_files(dir, [".pkl", ".gz"]):
        basename = os.path.basename(os.path.splitext(path)[0])
        dfs[basename] = pd.read_pickle(path)
    return dfs

def extract_pickled_dir(dir: str):
    for path in list_files(dir, [".pkl", ".gz"]):
        fp = os.path.splitext(path)[0]
        fp = fp if fp.endswith(".pkl") else fp + ".pkl"
        df:pd.DataFrame = pd.read_pickle(path)
        df.to_pickle(fp)
    