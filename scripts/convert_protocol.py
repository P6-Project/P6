from argparse import ArgumentParser
from protocol_identifier.protocol import convert_j1939

import pandas as pd

if __name__ == "__main__":
    pd.options.mode.chained_assignment = None
    parser = ArgumentParser(description="Convert protocol xlsx")
    parser.add_argument("j1939_path")
    args = parser.parse_args()
    df: pd.DataFrame = pd.read_excel(args.j1939_path, skiprows=3, sheet_name="SPNs & PGNs", usecols=[
        "PGN", "PGN Data Length", "SPN Position in PGN", 
        "SPN", "SPN Length", "Resolution", "Offset", 
        "Data Range", "Units"
        ])
    
    cdf = convert_j1939(df)
    cdf.to_pickle("./j1939.pkl")
    