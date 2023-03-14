import argparse
import pickle
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

argparser = argparse.ArgumentParser(
        prog='Pattern Recognizer Model',
        description='Creates a model using the data')

argparser.add_argument("file")
args = argparser.parse_args()

with open(args.file, "rb") as f:
    modelData, target = pickle.load(f)

array = []
# flatten the data
for matrix in modelData:
    array.append(np.concatenate(matrix))

X = np.array(array)
Y = np.array(target)

predictionArray = []

for i in range(100):
    X, Y = shuffle(X, Y)
    # Create a classifier: a support vector classifier
    clf = svm.SVC()

    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.15, shuffle=False
    )

    clf.fit(X_train, y_train)

    predictionArray.append(clf.score(X_test, y_test))

print("Confidence:", np.average(predictionArray))

