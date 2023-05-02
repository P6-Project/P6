import array
import binascii
import random
import secrets
import struct
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from enum import Enum

import os
import pickle
import warnings


def knn_train(data : pd.DataFrame, target : str = "Label", test_size : float = 0.2, random_state : int = 42):
    X = data[['ID', 'Data']]  # Features
    y = data['Label']  # Target variable
    
    # Split the dataset into training (70%) and testing (30%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Standardize the features to improve KNN performance
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # Create the KNN classifier with k=5 (you can experiment with different k values)
    knn_classifier = KNeighborsClassifier(n_neighbors=5)

    # Train the classifier using the training data
    knn_classifier.fit(X_train, y_train)
    pickle.dump(knn_classifier, open("./data/models/knn_model.pkl", "wb"))
    # Make predictions on the test set
    y_pred = knn_classifier.predict(X_test)

    # Evaluate the classifier's performance
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))








def filter_data_IDnum(data : pd.DataFrame, ID : int):
    """Filters data based on numbers of IDs that should be equal to ID"""
    data_dict = {}
    new_data = pd.DataFrame()
    for id in data["ID"]:
        data_dict[id] = data_dict.get(id, 0) + 1
    for key, value in data_dict.items():
        if value > data["ID"].count() / 100:
            new_data = new_data.append(data.loc[data["ID"] == key], ignore_index=True)
    return new_data


class Padding_side(Enum):
    left = 0
    right = 1

def bin_string_to_bigEndianHex(lst_hex : list[str]):
    """Converts hex string to big endian"""
    for i in range(len(lst_hex)):
        padded_hex = lst_hex[i][2:].zfill(6)
        b_e_hex = '0x' + "".join(reversed([padded_hex[i:i+2] for i in range(0, len(padded_hex), 2)]))        
        lst_hex[i] = b_e_hex
    return lst_hex
    

def alter_short_proto(data : pd.DataFrame, padding_range = [0x10000, 0x1FFFF], padding_side : Padding_side = Padding_side.left):
    """Takes in a dataframe and alters the ID's to be 29 bits long
    padding determines what string to pad from a list of string,
    and padding_side determines the side to pad"""
    #generate 10 random numbers from range
    id_padding_map = {}
    padded_str = ""
    padding_list = [str(hex(random.randint(padding_range[0], padding_range[1])) for _ in range(10))]
    if(padding_side is Padding_side.right):
        padding_list = bin_string_to_bigEndianHex(padding_list)
    #randomly apply padding to ID's, but same padding to same ID's
    for id in data["ID"].unique():
        if id is not type(str):
            data["ID"].apply(lambda x: str(hex(x)))
        padding = random.choice(padding_list)
        if padding_side is Padding_side.right:
            padded_str = id + padding
        elif padding_side is Padding_side.left:
            padded_str = padding + id
        id_padding_map[id] = padded_str
            

def main():
    warnings.filterwarnings("ignore")
    # Load data
    should_run = True
    # for files in os.listdir("./data/dfs"):
    #     if files.find("vehicle_data_ID_100") != -1:
    #         knn_train(pd.read_pickle("./data/dfs/" + files))
    #         should_run = False
    data = pd.DataFrame()
    for files in os.listdir("./data/dfs"):
        if files.find("timeNormalized") != -1 or files.find("rand_data_data") != -1 and should_run == True and files.find("normal_run") == -1:
            print(files)
            
            #construct vector for vehicle with most common ID's
            vehicle_df = pd.DataFrame()
            vehicle = pd.read_pickle("./data/dfs/" + files)
            if(vehicle["ID"].dtypes == "str"):
                vehicle["ID"] = vehicle["ID"].apply(lambda x: int(x, 16))
            if(vehicle["Data"].dtypes == "str"):
                vehicle['Data'] = vehicle['Data'].apply(lambda x: int(x, 16))
            if files.find("Kenworth") != -1:
                print(vehicle["Label"].unique())
            ID_dict = {}
            for id in vehicle["ID"]:
                ID_dict[id] = ID_dict.get(id, 0) + 1
            #if a value in the dictionary is greater than 100, add it to the dataframe
            for key, value in ID_dict.items():
                if value > vehicle["ID"].count() / 500:
                    if files.find("rand_data_data") != -1:
                        print(key, value)
                    vehicle_df = vehicle_df.append(vehicle.loc[vehicle["ID"] == key], ignore_index=True)
            #append the dataframe to the data
            data = data.append(vehicle_df, ignore_index=True)
    print(data.head(5000))
    #save the data
    data.to_pickle("./data/dfs/vehicle_data_ID_100.pkl")
    #knn_train(data)   
    
    

#range of ID padding: 10000 -> 1FFFF   

if __name__ == "__main__":
    bin_string_to_bigEndianHex(["0x1FFFFF", "0x100000"])    
    
                
            
    
    
    