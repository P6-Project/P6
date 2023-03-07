from loader import loadLoxam
import argparse
import pickle


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog = 'Loxam Data Extractor',
        description = 'Converts to Dataframe')

    argparser.add_argument("folder")
    argparser.add_argument("out")
    args = argparser.parse_args()
    
    loxamData = loadLoxam(args.folder)
    with open(args.out, "wb") as f:
        pickle.dump(loxamData, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(loxamData)
