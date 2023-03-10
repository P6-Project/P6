from loader import load_loxam_file
import os
import argparse
import pickle

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog = 'Loxam Data Extractor',
        description = 'Converts to Dataframe')

    argparser.add_argument("folder")
    argparser.add_argument("out")
    args = argparser.parse_args()
    
    for file in os.listdir(args.folder):
        loxamData = load_loxam_file(args.folder, file)
        file = file[:-4]
        path = os.path.join(args.out, file) + ".pkl"
        with open(path, 'wb') as f:
            pickle.dump(loxamData, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(loxamData)

