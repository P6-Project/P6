from data import load_pickled_dir
import argparse
import pandas as pd
import os

parser = argparse.ArgumentParser(description="P6 Protocol Identifier Proof of Concept")
parser.add_argument("path", help="Can be dir or file")
parser.add_argument("--relplot", help="Generate relplot")
parser.add_argument("--hist", help="Generate Histograms")
parser.add_argument("--model", help="run model", action="store", const="SVM", default="", nargs="?")

args = parser.parse_args()


