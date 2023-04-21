from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from protocol_identifier.data import load_pickled_dir
import os
import pandas as pd

def random_forrest_model_creator(
        output_path="./data/models", 
        delimiters=["timeNormalized", "rand_data_noise"], 
        pickle_path_dfs="./data/dfs",
        train_test_split_params={"test_size": 0.3, "random_state": 42},
        rf_params={"n_estimators": 100, "random_state": 42}
        ):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    dfs : dict = load_pickled_dir(pickle_path_dfs, delimiters=delimiters)
    dfs = dfs.values()
    dfs_pruned = []
    for df in dfs:
        print(df)
        print(df.keys())
        if df.Name.find("rand_data_noise") != -1:
            dfs_pruned.append(df)
            continue
        if df.iloc[:,-1].isin(["Unknown"]).any():
            print("Unknown label found, skipping " + df.Name)
            continue
        dfs_pruned.append(df)
            
    combined_df = pd.concat(dfs, axis=0, ignore_index=True)
    X = combined_df['ID']
    y = combined_df['Label']
    X = X.apply(lambda x: int(x, 16))
    X = X.to_frame()
    X_train, X_test , y_train, y_test = train_test_split(
        X, y, 
        test_size=train_test_split_params["test_size"] ,
        random_state=train_test_split_params["random_state"]
        )
    rf = RandomForestClassifier(
        n_estimators=rf_params["n_estimators"], 
        random_state=rf_params["random_state"]
        )
    rf.fit(X_train, y_train)
    save_model(rf, output_path ,"randomForrest")
    predictions = rf.predict(X_test)
    
    accuracy = (predictions == y_test).mean()
    print("Accuracy: " + str(accuracy))


def save_model(model : str, dest : str, filename : str):
    pd.to_pickle(model, dest + "/"  + filename + ".pkl")


def predictRF(data: pd.DataFrame, model ="./data/models/randomForrest.pkl") -> str:
    res_dict = {}
    try:
        model = pd.read_pickle(model)
    except FileNotFoundError:
        return "No model found, plz train benis"
    result = model.predict(data)
    for e in result:
        res_dict[e] = res_dict.get(e, 0) + 1
    for key in res_dict:
        res_dict[key] = res_dict[key] / len(result)
        if res_dict[key] > 0.5:
            return key
    return "Unknown"



    
    