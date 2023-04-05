import os

from protocol_identifier.data import converter
from protocol_identifier.data import load_loxam, load_renault

def helper_converter(files: str, dump: str, com:bool=False):
    if not os.path.exists(dump):
        os.mkdir(dump)
    converter({
            files + "csv/loxam.csv": (load_loxam, False, []), files + "csv/renault.csv": (load_renault, False, [])
        }, dump, com)