from sklearn import svm
import pandas as pd

def main():
    clf = svm.SVC(gamma = 0.001, C = 100.)

    data = pd.read_csv('data.csv')

    data = data.iloc[0:5000]

    X = data.iloc[:, 0:64]
    Y = data.iloc[:, 64]

    clf.fit(X, Y)

    pr = clf.predict(X)
    print(sum(pr==Y))

if __name__ == "__main__":
    main()
