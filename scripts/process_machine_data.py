import argparse
from protocol_identifier.verification import find_used_spns, find_usable_spns, read_loxam_machine_data
import time

argparser = argparse.ArgumentParser(
        prog='Loxam Data Extractor',
        description='Finds pgns')

argparser.add_argument("j1939_path")
argparser.add_argument("machine_data")
args = argparser.parse_args()

machine_data_as_df = read_loxam_machine_data(args.machine_data)

start = time.time()

(refined_machine_data, used_spns) = find_used_spns(args.j1939_path, machine_data_as_df)

list = find_usable_spns(refined_machine_data, used_spns)

print(list)
print(time.time() - start)
