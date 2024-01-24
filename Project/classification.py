import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import seaborn
seaborn.set()


'''
Classification (GaussianNB, knn, random forest, svc)
'''
summary = pd.read_csv('dataset/summary.csv')
class_feature = ['gender']
for feature in class_feature:
    X_train, X_valid, y_train, y_valid = train_test_split(summary[['frequency']].values, summary[feature].values)
    GaussianNB = GaussianNB()
    knn = KNeighborsClassifier(3)
    rf = RandomForestClassifier(20, max_depth=4)
    svc = SVC(kernel='linear')

    models = {"GaussianNB": GaussianNB, "knn": knn, "rf": rf, "svc": svc}
    for model_name, model in models.items():
        model.fit(X_train, y_train)
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_valid, y_valid)
        print(feature + ' ' + model_name + ' train score = ' + str(train_score))
        print(feature + ' ' + model_name + ' test score = ' + str(test_score))
