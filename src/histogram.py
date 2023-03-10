import os
import pandas as pd
import matplotlib.pyplot as plt

def create_all_graphs(input_dir, output_dir):
    for file in os.listdir(input_dir):
        file_dict = create_dict_can_pkl(input_dir + file)
        diagram = create_bar_diagram_can_ids(file_dict, file)
        diagram.savefig(output_dir + file[:-4] + ".png", format="png", dpi=1200)

def create_bar_diagram_can_ids(can_id_dict, file_name):
    plt.clf()
    plt.figure().set_figwidth(5 + (len(can_id_dict)/10))
    plt.bar(can_id_dict.keys(), can_id_dict.values(), 0.5)
    plt.xticks(rotation='vertical')
    plt.title(file_name)
    plt.xlabel('CAN Id')
    plt.ylabel('Quantity')
    plt.margins(0.01)
    plt.tight_layout() # Else it cuts half of the bottom text.
    return plt

def create_dict_can_pkl(file):
    df = pd.read_pickle(file)

    can_id_dict = dict()
    
    for index, row in df.iterrows():
        if row['ID'] in can_id_dict:
            can_id_dict[row['ID']] += 1
            continue
        else:
            can_id_dict[row['ID']] = 1

    return can_id_dict

create_all_graphs("../../data/", "../../graphs/")
diagram = create_bar_diagram_can_ids(create_dict_can_pkl("../../data/JCB 19C1E mini loader off.pkl"), "JCB 19C1E mini loader ignition test")
diagram.show()
