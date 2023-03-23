import pandas as pd


def compareKnownPGNs(pgn: pd.DataFrame, machines: pd.DataFrame):
    matches = pd.DataFrame()
    matches1 = pd.DataFrame()
    print(pgn)
    for m in machines["Machine"].unique():
        print(f"Machine: {m} has {len(machines[machines['Machine'] == m])} IDs")
        matches = pd.merge(
            pgn,
            machines[machines["Machine"] == m],
            left_on="PGN",
            right_on="ID",
            how="inner",
        )
        matches1 = pd.concat([matches1, matches], ignore_index=True)
    for m in matches1["Machine"].unique():
        print(f"{m} has {len(matches1[matches1['Machine'] == m])} matches")
    
    
    
    

def hex_to_bin(hex_string):
    binary = bin(int(hex_string, 16))[2:]
    return '{:0>29}'.format(binary)

def bin_to_PGN(bin_string):
    return bin_string[9:25]

def bin_to_int(bin_string):
    return int(bin_string, 2)

def main(flag: int = 0 ):
    pgn : pd.DataFrame = pd.read_pickle("./pgn.pkl")
    if flag == 1:
        pgn = pgn.drop_duplicates()
    else:
        x = 0
        for i, p in enumerate(pgn):
            if i == 0:
                continue
            if p == pgn[i-1]:
                x += 1
        print(x)
    machine : pd.DataFrame = pd.read_pickle("./data.pkl")
    m : pd.DataFrame = machine.loc[:, ["Machine", "ID"]]
    uniqueID: pd.DataFrame = pd.DataFrame(columns=["Machine", "ID"])
    i = 0
    for machine in m["Machine"].unique():
        for id in m[m["Machine"] == machine]["ID"].unique():
            uniqueID = pd.concat([uniqueID, pd.DataFrame({"Machine": [machine], "ID": [id]})], ignore_index=True)
    uniqueID["ID"] = uniqueID["ID"].apply(hex_to_bin).apply(bin_to_PGN).apply(bin_to_int)
    compareKnownPGNs(pgn, uniqueID)

if __name__ == "__main__":
    main()
    main(1)
    
        
               
        
    
    

    
        