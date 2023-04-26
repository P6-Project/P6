import pandas as pd

def can_open_range():
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