from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np

def make_model(X_train, y_train):
    # Create our imputer to replace missing values with the mean e.g.
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp = imp.fit(X_train)

    # Impute our data, then train
    X_train_imp = imp.transform(X_train)
    clf = RandomForestClassifier(n_estimators=10)
    clf = clf.fit(X_train_imp, y_train)
    return imp, clf

def data_inc(X, k):
    n,m = X.shape
    X_inc = np.zeros((n,m*k))
    # 이전 없는 데이터는 nan으로 채움
    for j in range(m, m*k):
        X_inc[0,j] = np.nan
    # 기존 데이터
    for i in range(n):
        for j in range(m):
            X_inc[i,j] = X[i,j]

    # 이전 데이터 추가
    for i in range(1,n):
        for j in range(m, m*k):
            X_inc[i,j] = X_inc[i-1,j-m]

    return X_inc

if __name__ == '__main__':
    df = pd.read_csv("data\\data7x7_1000.csv")
    dataset = df.to_numpy()[:, 1:]
    n_data = len(dataset)
    X = dataset[:, :-2]
    X = data_inc(X, 5)
    #print(X[:10])
    y1 = dataset[:, -2]
    y2 = dataset[:, -1]
    X_train = X[:int(n_data * 0.75), :]
    X_test = X[int(n_data * 0.75):, :]
    y1_train = y1[:int(n_data * 0.75)]
    y1_test = y1[int(n_data * 0.75):]
    y2_train = y2[:int(n_data * 0.75)]
    y2_test = y2[int(n_data * 0.75):]

    imp1, clf1 = make_model(X_train, y1_train)
    imp2, clf2 = make_model(X_train, y2_train)

    y1_predict = clf1.predict(imp1.transform(X_test))
    y2_predict = clf2.predict(imp2.transform(X_test))
    print("leader acc:", end=" ")
    print((y1_test == y1_predict).sum()/len(y1_predict)*100)
    print()
    print("team   acc:", end=" ")
    print((y2_test == y2_predict).sum()/len(y2_predict)*100)
