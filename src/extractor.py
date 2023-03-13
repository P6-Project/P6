import argparse
import pickle

import pandas as pd

from data import processData, readDirCanData

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog="Loxam Data Extractor", description="Converts to Dataframe"
    )

    argparser.add_argument("folder")
    argparser.add_argument("sampleSize", type=int)
    argparser.add_argument("out")
    args = argparser.parse_args()

    dfs = readDirCanData(args.folder, 10000)
    df = pd.concat(processData(dfs, args.sampleSize))

    with open(args.out, "wb") as f:
        pickle.dump(df, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(df)
