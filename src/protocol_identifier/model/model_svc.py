import pickle
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def train_model() -> SVC:
    train_dfs = []
    test_dfs = []
    for filename in os.listdir("./data/dfs"):
        if filename.find("binaryMatrix") != -1:
            try:
                df: pd.DataFrame = pd.read_pickle(
                    os.path.join("./data/dfs", filename))
                if (df.iloc[:, -1] == "Unknown").any():
                    print("Unknown label found, skipping" + filename)
                    continue
                train_df, test_df = train_test_split(
                    df, test_size=0.3, random_state=42)
                train_dfs.append(train_df)
                test_dfs.append(test_df)
            except ValueError:
                continue

    train_data = pd.concat(train_dfs, axis=0, ignore_index=False).fillna(0)
    test_data = pd.concat(test_dfs, axis=0, ignore_index=False).fillna(0)
    X_train = train_data.iloc[:, :-1]
    y_train = train_data.iloc[:, -1]

    X_test = test_data.iloc[:, :-1]
    y_test = test_data.iloc[:, -1]
    print(X_test.head(100))
    print(y_test.head(100))
    svm = SVC(kernel='linear', C=1, random_state=42)
    svm.fit(X_train, y_train)
    with open("./data/modelColumns.pkl", "wb") as f:
        pickle.dump(train_data.columns, f)
    with open("./data/model.pkl", "wb") as f:
        pickle.dump(svm, f)

    score = svm.score(X_test, y_test)
    print("Accuracy: " + str(score))


def predict(df: pd.DataFrame) -> str:
    with open("./data/model.pkl", "rb") as f:
        svm = pickle.load(f)
    with open("./data/modelColumns.pkl", "rb") as f:
        feature_names = pickle.load(f)
    df = df.reindex(columns=feature_names, fill_value=0)
    df = df.fillna(0)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    score = svm.score(X, y)
    print("Accuracy: " + str(score))
    prediction = svm.predict(X)
    predict_protocol = {}
    for p in prediction:
        predict_protocol[p] = predict_protocol.get(p, 0) + 1
    highest_protocol = max(predict_protocol, key=predict_protocol.get)
    return highest_protocol if score > 0.7 else "Unknown"


def predict_from_file(filename: str) -> str:
    df = pd.read_pickle(os.path.join("./data/dfs", filename))
    return predict(df)


if __name__ == "__main__":
    # if not os.path.exists("./data/model.pkl"):
    train_model()
    for files in os.listdir("./data/dfs"):
        if files.find("binaryMatrix") != -1:
            print("predicting: " + files + "")
            print(predict_from_file(files))