import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd


#loading data
print("loading cars")
with open("./loxam.pkl", "rb") as f:
    dataframe: pd.DataFrame = pickle.load(f)
	

dataframe["ID"] = dataframe["ID"].apply(lambda x: int(x, 16))
Target = dataframe["Name"]
dataframe = dataframe.drop("Name", axis=1).drop("Source", axis=1).drop("Action", axis=1)



# Splitting data
print("splitting data")
data_train, data_test, target_train, target_test = train_test_split(dataframe, Target, test_size=0.2)

#  Setup and training
print("setup and training")
clf = RandomForestClassifier()

clf.fit(data_train, target_train)
print("Prediction: ", clf.predict(data_test))
print("Target Values: ", target_test)
print("Confidence: ", clf.score(data_test, target_test))