from protocol_identifier.protocol import find_j1939_protocol_matches

from argparse import ArgumentParser
import pandas as pd
import numpy as np
import time

class Predictor:
    def predict(self, X) -> np.ndarray: # type: ignore
        pass

if __name__ == "__main__":
    start = time.time()
    parser = ArgumentParser(description="Identify Protocol and usable data points")
    parser.add_argument("vehicle_path")
    parser.add_argument("model_path")
    parser.add_argument("j1939_path")
    args = parser.parse_args()

    vh: pd.DataFrame = pd.read_pickle(args.vehicle_path)
    model: Predictor = pd.read_pickle(args.model_path)
    
    protocol: pd.DataFrame = pd.read_pickle(args.j1939_path)
    
    ids = vh["ID"].apply(lambda x: int(x, 16)).to_frame()
    
    values, count = np.unique(model.predict(ids), return_counts=True)
    
    prediction = values[count.argmax()]

    if prediction in ["J1939"]:
        print(prediction)
        matches = find_j1939_protocol_matches(protocol, vh)
        print(matches.to_dataframe())
    else:
        print(f"{prediction} is not supported")
    print(time.time() - start)
