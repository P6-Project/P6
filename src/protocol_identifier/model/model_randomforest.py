from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
import pandas as pd
from protocol_identifier.data.pkl_reader import load_pickled_dir

def random_forrest_model_creator(source : str = "./data/dfs"):
    if not os.path.exists("./data/models"):
        os.makedirs("./data/models")
    dfs = load_pickled_dir(source)
    for key in dfs.keys():
        df = dfs[key]
        if (df.iloc[:, -1] == "Unknown").any():
            print("Unknown label found, skipping" + key)
            del dfs[key]
    combined_df = pd.concat(dfs, axis=0, ignore_index=True)
    X = combined_df['ID']
    y = combined_df['Label']
    X = X.apply(lambda x: int(x, 16))
    X = X.to_frame()
    X_train, X_test , y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    save_model(rf, "randomForrest")
    predictions = rf.predict(X_test)
    
    accuracy = (predictions == y_test).mean()
    print("Accuracy: " + str(accuracy))
    

def save_model(model, filename):
    pd.to_pickle(model, "./data/models/" + filename + ".pkl")


def predict(model, data):
    return model.predict(data)

if __name__ == "__main__":
    #random_forrest_model_creator()
    for files in os.listdir("./data/dfs"):
        if files.find("timeNormalized") != -1:
            resDict = {}
            print(files)
            df : pd.DataFrame = pd.read_pickle(os.path.join("./data/dfs", files))
            res = predict(pd.read_pickle("./data/models/randomForrest.pkl"), df['ID'].apply(lambda x: int(x, 16)).to_frame())
            for e in res:
                resDict[e] = resDict.get(e, 0) + 1    
            print(resDict)
    
    