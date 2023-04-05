from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
import pandas as pd


def random_forrest_model():
    dfs = []
    for filename in os.listdir("./data/dfs"):
        print(filename)
        if filename.find("timeNormalized") != -1:
            df: pd.DataFrame = pd.read_pickle(
                os.path.join("./data/dfs", filename))
            if (df.iloc[:, -1] == "Unknown").any():
                print("Unknown label found, skipping" + filename)
                continue
            dfs.append(df)
    combined_df = pd.concat(dfs, axis=0, ignore_index=True)
    X = combined_df['ID']
    y = combined_df['Label']
    X = X.apply(lambda x: int(x, 16))
    X = X.to_frame()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    predictions = rf.predict(X_test)

    accuracy = (predictions == y_test).mean()
    print("Accuracy: " + str(accuracy))


if __name__ == "__main__":
    random_forrest_model()
