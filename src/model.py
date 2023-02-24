import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import random

#loading data
print("loading cars")
with open("../cars.pkl", "rb") as f:
    cars: dict = pickle.load(f)
	
data = []
target = []

#Formatting Data
print("formatting cars")
for i, (car, car_data) in enumerate(cars.items(), 1):
    for d in car_data:
        random.shuffle(d)
        data.append(d)
        target.append(i)
minlen = min(len(d) for c, cd in cars.items() for d in cd) - 1
data = [d[:minlen] for d in data]

# Splitting data
print("splitting data")
data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.2)

#  Setup and training
print("setup and training")
clf = RandomForestClassifier()
clf.fit(data_train, target_train)
print("Prediction: ", clf.predict(data_test))
print("Target Values: ", target_test)
print("Confidence: ", clf.score(data_test, target_test))