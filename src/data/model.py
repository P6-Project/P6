import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

def train_model():
    for filename in os.listdir("./data/dfs"):
        train_dfs = []
        test_dfs = []
        cols = []
        for filename in os.listdir("./data/dfs"):
            if filename.find("binaryMatrix") != -1:
                try:
                    df = pd.read_pickle(os.path.join("./data/dfs", filename))
                    train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)
                    train_dfs.append(train_df)
                    test_dfs.append(test_df)
                except ValueError:
                    continue

    train_data = pd.concat(train_dfs, axis=0, ignore_index=False).fillna(0)
    test_data = pd.concat(test_dfs, axis=0, ignore_index=False).fillna(0)
    X_train = train_data.iloc[:,:-1]
    y_train = train_data.iloc[:,-1]

    X_test = test_data.iloc[:,:-1]
    y_test = test_data.iloc[:,-1]
    print(X_test.head(100))
    print(y_test.head(100))
    svm = SVC(kernel='linear', C=1, random_state=42)
    svm.fit(X_train, y_train)

    score = svm.score(X_test, y_test)
    print("Accuracy: " + str(score))
    
if __name__ == "__main__":
    train_model()