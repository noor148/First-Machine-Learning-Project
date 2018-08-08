from sklearn import svm
import pandas as pd
from sklearn.externals import joblib
import numpy as np

def train_model():
    clf = svm.SVC(gamma = 0.001, C = 100.)

    data = pd.read_csv('data.csv')

    data = data.iloc[0:5000]

    X = data.iloc[:, 0:64]
    Y = data.iloc[:, 64]

    clf.fit(X, Y)

    return clf

def main():
    clf = svm.SVC(kernel = 'rbf')

    data = pd.read_csv('data.csv')

    data = data.iloc[0:1000]

    X = data.iloc[:, 0:64]
    Y = data.iloc[:, 64]

    print(type(X))
    print(type(Y))

    clf.fit(X, Y)
    
    res = clf.predict(X)
    print(res)
    print(Y)

    joblib.dump(clf, 'svm.pkl')    

if __name__ == "__main__":
    main()
