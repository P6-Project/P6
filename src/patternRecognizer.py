import pickle
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

with open("./data.pkl", "rb") as f:
    file: pd.DataFrame = pickle.load(f)

target = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
          3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
          4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
          6, 6, 6, 6,
          7, 7]
array = []
# flatten the data
for matrix in file:
    array.append(np.concatenate(matrix))

X = np.array(array)
Y = np.array(target)
X, Y = shuffle(X, Y)
# Create a classifier: a support vector classifier
clf = svm.SVC()

# Split data into 50% train and 50% test subsets
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.35, shuffle=False
)

# Learn the digits on the train subset
clf.fit(X_train, y_train)

# Predict the value of the digit on the test subset
print("Prediction: ", clf.predict(X_test))
print("Target Values: ", y_test)
print("Confidence: ", clf.score(X_test, y_test))

print("RANDOM FOREST")

rbf = RandomForestClassifier()

rbf.fit(X_train, y_train)
print("Prediction: ", clf.predict(X_test))
print("Target Values: ", y_test)
print("Confidence: ", clf.score(X_test, y_test))

