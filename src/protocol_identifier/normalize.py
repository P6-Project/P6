from typing import Sequence


def norm_time(time: Sequence[str], limit: int):
    first = 0
    nTC = []
    for i, t in enumerate(time):
        norm = milis(t) - milis(time[first])
        if i == limit:
            first = i
        if i == first:
            nTC.append(0)
        else:
            nTC.append(norm)
    return nTC

def milis(time: str):
    "%H:%M:%S.%f to miliseconds"
    split = time.split(":")
    hour = int(split[0]) * 3_600_000
    minute = int(split[1]) * 60_000
    split = split[2].split(".")
    second = int(split[0]) * 1000
    milis = int(int(split[1]) / 1000)
    return hour + minute + second + milis 