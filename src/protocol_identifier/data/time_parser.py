from datetime import datetime
import pytz

TIMEFORMAT = "%H:%M:%S.%f"

def loxam_date_parser(row: list):
    time: str = row[1] + " " + row[2]
    d = (time[:-4] + time[-3:]).replace(",", ".")
    return datetime.strptime(d, "%d/%m/%Y %H:%M:%S.%f").strftime(TIMEFORMAT)

def unix_time_parser(date: str):
    d: float = float(date.replace("(", "").replace(")", ""))
    time = datetime.fromtimestamp(d, tz=pytz.utc)
    return time.astimezone(pytz.timezone("Europe/Copenhagen")).strftime(TIMEFORMAT)

def date_parser(time: str):
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f").strftime(TIMEFORMAT)