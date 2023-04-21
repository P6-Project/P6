from sklearn.ensemble import RandomForestClassifier
from argparse import ArgumentParser
import pandas as pd
from protocol_identifier.model import predictRF
from protocol_identifier.verification import find_used_spns, find_usable_spns

def identify(vehicle_path: str, model_path: str, j1939excel_path: str):
    vh = pd.read_pickle(vehicle_path)
    protocol = predictRF(vh, model_path)

    if protocol != "J1939":
        raise Exception("Dataset not J1939")
    refined_machine_data, used_spns = find_used_spns(j1939excel_path, vh)
    return find_usable_spns(refined_machine_data, used_spns)

if __name__ == "__main__":
    #parser = ArgumentParser(description="Identify Protocol and usable data points")
    #parser.add_argument("model_path")
    #parser.add_argument("vehicle_path")
    #parser.add_argument("j1939_path")
    #args = parser.parse_args()

    try:
        #print(identify(args.vehicle_path, args.model_path, args.j1939_path))
        print(identify("C:\\Users\\magnu\\Downloads\\2015 Kenworth T660_run.pkl.gz","C:\\Users\\magnu\\Downloads\\randomForrest.pkl", "C:\\Users\\magnu\\Desktop\\J1939DA_201802.xls"))
    except Exception as e:
        print(e)