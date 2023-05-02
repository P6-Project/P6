import pickle
from sklearn import linear_model
from sklearn import metrics
from sklearn import model_selection
from sklearn import preprocessing
import pandas as pd
import os

def linear_regression_model_creator(data: pd.DataFrame, target: str = "Label", test_size: float = 0.2, random_state: int = 42):
    X = data["ID"].to_frame()
    print(X.head(5000))
    le = preprocessing.LabelEncoder()
    y = data[target]
    y_encoded = le.fit_transform(y)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y_encoded, test_size=test_size, random_state=random_state)
    model = linear_model.LogisticRegression()
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
    return model

def test_model_acc(model: linear_model.LinearRegression, data : pd.DataFrame, target: str = "Label"): 
    a, b = 0, 0
    X = data["ID"].to_frame()
    if(X["ID"].dtype != "int64"):
        X["ID"] = X["ID"].apply(lambda x: int(x, 16)).to_frame()
    le = preprocessing.LabelEncoder()
    y = data[target]
    y_encoded = le.fit_transform(y)
    y_pred = model.predict(X)
    print("Mean Absolute Error:", metrics.mean_absolute_error(y_encoded, y_pred))
    print("Mean Squared Error:", metrics.mean_squared_error(y_encoded, y_pred))

def predict(model : linear_model.LinearRegression, data : pd.DateOffset, target : str = "Label") -> str:
    X : pd.DataFrame = data.drop(target, axis=1)
    X.loc["ID"].apply(lambda x: int(x, 16)).to_frame()
    return model.predict(X)

def save_model(model : linear_model.LinearRegression, name : str, path : str = "./data/models/"):
    path = os.path.join(path, name + ".pkl")
    with open(path, "wb") as f:
        pickle.dump(model, f)

def load_model(name : str, path : str = "./data/models/"):
    path = os.path.join(path, name + ".pkl")
    with open(path, "rb") as f:
        return pickle.load(f)


