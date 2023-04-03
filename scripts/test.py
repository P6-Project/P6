from protocol_identifier.graph import id_pattern
import pandas as pd

FILES = "./test/test_files/"
df = pd.read_pickle(FILES + "pkl/loxam.pkl")

id_pattern(df, "benis.png")