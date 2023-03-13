from datetime import datetime

TIMEFORMAT = "%H:%M:%S.%f"

def CSUDateParser(date: str):
    d: float = float(date.replace("(", "").replace(")", ""))
    return datetime.fromtimestamp(d).strftime(TIMEFORMAT)

def CSUIDParser(id: str):
    return id.split("#")[0]

def loxamDateParser(time: str):
    d = (time[:-4] + time[-3:]).replace(",", ".")
    return datetime.strptime(d, "%d/%m/%Y %H:%M:%S.%f").strftime(TIMEFORMAT)

def dateParser(time: str):
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f").strftime(TIMEFORMAT)

def renaultIDParser(id: str):
    return id[2:]