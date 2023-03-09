import pandas as pd
import matplotlib.pyplot as plt

def create_dict_can_pkl():
    df = pd.read_pickle("../../data/loxam1.pkl")

    can_id_dict = dict()
    
    for index, row in df.iterrows():
        if row['ID'] in can_id_dict:
            can_id_dict[row['ID']] += 1
            continue
        else:
            can_id_dict[row['ID']] = 1

    return can_id_dict

def create_bar_diagram_can_ids(can_id_dict):
    plt.bar(can_id_dict.keys(), can_id_dict.values(), 0.5)
    plt.xticks(rotation='vertical')
    plt.title("Can ID data")
    return plt

diagram = create_bar_diagram_can_ids(create_dict_can_pkl())
diagram.show()
