import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

# python3 weather_city.py monthly-data-labelled.csv monthly-data-unlabelled.csv labels.csv

def main():
    labelled = pd.read_csv(sys.argv[1])
    unlabelled = pd.read_csv(sys.argv[2])

    X = labelled.loc[:, 'tmax-01':'snwd-12']
    y = labelled['city']
    X_unlabelled = unlabelled.loc[:,'tmax-01':'snwd-12']
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)

    #model = KNeighborsClassifier(n_neighbors=10)
    #model = GaussianNB()
    model = RandomForestClassifier(n_estimators=500, min_samples_leaf=5)
    #model.fit(X_train, y_train)
    convert_model = make_pipeline(StandardScaler(), model)
    convert_model.fit(X_train, y_train)

    predictions = convert_model.predict(X_unlabelled)
    print("Score: ", convert_model.score(X_valid, y_valid))

    df = pd.DataFrame({'truth': y_valid, 'prediction': model.predict(X_valid)})
    # print(df[df['truth'] != df['prediction']])

    pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)

if __name__ == '__main__':
    main()