import pandas as pd
import os
import sklearn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
import matplotlib.pyplot as plt
from sklearn import tree
import numpy as np

def get_model():
    model: RandomForestClassifier = load_random_forest_model()
    if model is None:
        # model = train_model()
        pass
    else:
        print(model.n_features_in_, model.n_outputs_)

        fn = model.feature_names_in_
        cn = np.unique(model.classes_).astype(str)

        for idx, trees in enumerate(model.estimators_):
            fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), dpi=800)
            tree.plot_tree(trees,
                      feature_names=fn,
                      class_names=cn,
                      filled=True,
                      ax=axes)
            fig.savefig(f'rf_individualtree_{idx}.png')
    
    
    
    
    
def load_random_forest_model():
    print(os.getcwd())
    for files in os.listdir("../../data/models"):
        if(files.find("randomForrest") != -1):
            return pd.read_pickle("../../data/models/" + files)
    return None

if __name__ == "__main__":
    get_model()