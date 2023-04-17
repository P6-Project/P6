import argparse
from protocol_identifier.processing import find_used_spns, find_usable_spns


argparser = argparse.ArgumentParser(
        prog='Loxam Data Extractor',
        description='Finds pgns')

argparser.add_argument("excelpath")
argparser.add_argument("machinedata")
args = argparser.parse_args()

(machine_data, used_spns) = find_used_spns(args.excelpath, args.machinedata)

list = find_usable_spns(machine_data, used_spns)

print(list)
