from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
import pandas as pd

def load_pickled_dir(path, delimiters=[]):
    dfs = []
    for files in os.listdir(path):
        for delimiter in delimiters:
            if files.find(delimiter) != -1:
                df = pd.read_pickle(os.path.join(path, files))
                df.Name = files
                dfs.append(df)
    return dfs


def random_forrest_model_creator(
        output_path="./data/models", 
        delimiters=["timeNormalized", "rand_data_noise"], 
        pickle_path_dfs="./data/dfs",
        train_test_split_params={"test_size": 0.3, "random_state": 42},
        rf_params={"n_estimators": 100, "random_state": 42}
        ):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    dfs : list[pd.DataFrame] = load_pickled_dir(pickle_path_dfs, delimiters=delimiters)
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
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    save_model(rf, "randomForrest")
    predictions = rf.predict(X_test)
    
    accuracy = (predictions == y_test).mean()
    print("Accuracy: " + str(accuracy))


def save_model(model, filename):
    pd.to_pickle(model, "./data/models/" + filename + ".pkl")


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



if __name__ == "__main__":
    #random_forrest_model_creator()
    for files in os.listdir("../../../data/dfs"):
        if files.find("timeNormalized") != -1:
            resDict = {}
            print(files)
            df : pd.DataFrame = pd.read_pickle(os.path.join("../../../data/dfs", files))
            res = predict(pd.read_pickle("./data/models/randomForrest.pkl"), df['ID'].apply(lambda x: int(x, 16)).to_frame())
            for e in res:
                resDict[e] = resDict.get(e, 0) + 1    
            print(resDict)
    
    