from datetime import datetime
import pytz

TIMEFORMAT = "%H:%M:%S.%f"

def CSUDateParser(date: str):
    d: float = float(date.replace("(", "").replace(")", ""))
    time = datetime.fromtimestamp(d, tz=pytz.utc)
    return time.astimezone(pytz.timezone("Europe/Copenhagen")).strftime(TIMEFORMAT)

def CSUIDParser(id: str):
    return id.split("#")[0]

def loxamDateParser(time: str):
    d = (time[:-4] + time[-3:]).replace(",", ".")
    return datetime.strptime(d, "%d/%m/%Y %H:%M:%S.%f").strftime(TIMEFORMAT)

def dateParser(time: str):
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f").strftime(TIMEFORMAT)

def renaultIDParser(id: str):
    return id[2:]