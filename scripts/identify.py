from protocol_identifier.processing import find_j1939_protocol_matches

from argparse import ArgumentParser
import pandas as pd
import numpy


class Predictor:
    def predict(self, X) -> numpy.ndarray: # type: ignore
        pass

if __name__ == "__main__":
    parser = ArgumentParser(description="Identify Protocol and usable data points")
    parser.add_argument("vehicle_path")
    parser.add_argument("model_path")
    parser.add_argument("j1939_path")
    args = parser.parse_args()

    vh: pd.DataFrame = pd.read_pickle(args.vehicle_path)
    model: Predictor = pd.read_pickle(args.model_path)
    
    protocol: pd.DataFrame = pd.read_pickle(args.j1939_path)
    
    prediction = numpy.bincount(model.predict(vh["ID"])).argmax()
    
    if prediction in ["J1939"]:
        matches = find_j1939_protocol_matches(protocol, vh)
        print(matches)
    else:
        print(f"{prediction} is not supported")
