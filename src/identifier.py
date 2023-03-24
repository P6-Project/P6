import pickle
import pandas as pd

def genCanOpen():
    return pd.Series([
        0,
        128,
        *list(range(129, 256)),
        256,
        *list(range(385, 512)),
        *list(range(513, 640)),
        *list(range(641, 768)),
        *list(range(769, 896)),
        *list(range(897, 1024)),
        *list(range(1025, 1152)),
        *list(range(1153, 1280)),
        *list(range(1281, 1408)),
        *list(range(1409, 1536)),
        *list(range(1537, 1694)),
        *list(range(1793, 1920)),
        ])



def ProtocolCertainty(ids: pd.Series, pgns: pd.Series):
    return ids.isin(pgns).mean()

def pgn(id: str):
    idLen = len(id)
    binId = f"{int(id, 16):08b}"
    if idLen == 8:
        binId = binId[3:-8]
    elif idLen == 7:
        binId = (binId.zfill(29))[3:-8]
    elif idLen == 3:
        binId = binId[2:]
    elif idLen == 2:
        binId = (binId.zfill(11))[2:]
    else:
        raise Exception(f"{idLen}, {binId}")
    return int(binId, 2)

if __name__ == "__main__":

    machines: pd.DataFrame  = pd.read_pickle("data.pkl")
    uniqueIDs: dict[str, pd.Series] = dict()

    for n in machines["Machine"].unique():
        m: pd.DataFrame = machines[machines["Machine"] == n]
        uniqueIDs[n] = m["ID"].drop_duplicates().apply(pgn)

    j1939: pd.Series = pd.read_excel("C:\\Users\\magnu\\Desktop\\J1939DA_201802.xls", skiprows=3, sheet_name="SPNs & PGNs", usecols=["PGN"])["PGN"].dropna().apply(int).drop_duplicates()
    canOpen = genCanOpen()

    ma = []
    p = []
    j = []
    o = []
    l = []

    for machine, ids in uniqueIDs.items():
        j19 = ProtocolCertainty(ids, j1939)
        ope = ProtocolCertainty(ids, canOpen)
        isJ1939 = j19 > ope 
        isNone = j19 == ope
        standard = "None"
        if isJ1939 and not isNone:
            standard = "J1939"
        elif not isNone:
            standard = "CanOpen"
        ma.append(machine)
        p.append(standard)
        j.append(j19 * len(ids))
        o.append(ope * len(ids))
        l.append(len(ids))

    pDf = pd.DataFrame({"Machine": ma, "Protocol": p, "J1939": j, "OpenCAN": o, "IDs": l})
    print(pDf)


