import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
import seaborn
seaborn.set()

'''
Linear Regression and SVR
'''
print('\n======= Score of Regression models =======')
summary = pd.read_csv('dataset/summary.csv')
reg_feature = ['age', 'height', 'bmi']

for feature in reg_feature:
    x = summary[['frequency']].values
    y = summary[feature].values
    X_train, X_valid, y_train, y_valid = train_test_split(x, y)

    lin_reg = LinearRegression(fit_intercept=True)
    knn = KNeighborsRegressor(3)
    rf = RandomForestRegressor(20, max_depth=4)
    svr = SVR(kernel='linear')
    # mlp = MLPRegressor(hidden_layer_sizes=(2, 2))
    # ConvergenceWarning: Stochastic Optimizer: Maximum iterations (200) reached and the optimization hasn't converged yet.

    models = {'lin': lin_reg, 'knn': knn, 'rf': rf, 'svr': svr}
    for model_name, model in models.items():
        model.fit(X_train, y_train)
        score = model.score(X_valid, y_valid)
        print(model_name + '\t' + feature + ' score = ' + str(score))
    
    # Plot the linear regression line for testing data
    plt.figure()
    plt.plot(X_valid, y_valid, '.', markersize=20)
    plt.plot(X_valid, lin_reg.predict(X_valid), linewidth=3)
    plt.xlabel('Step Frequency')
    plt.ylabel(feature)
    plt.legend(['Dataset', 'Regression Line'])
    plt.title('Linear regression for ' + feature + ' vs step frequency - testing data')
    plt.savefig('figures_regression/' + 'lin_reg_' + feature + '_test.jpg')
    plt.close()

    # Plot the linear regression line for training data
    plt.figure()
    plt.plot(X_train, y_train, '.', markersize=20)
    plt.plot(X_train, lin_reg.predict(X_train), linewidth=3)
    plt.xlabel('Step Frequency')
    plt.ylabel(feature)
    plt.legend(['Dataset', 'Regression Line'])
    plt.title('Linear regression for ' + feature + ' vs step frequency - training data')
    plt.savefig('figures_regression/' + 'lin_reg_' + feature + '_train.jpg')
    plt.close()

'''
Linear Regression with p-value and r^2
'''
print('\n===== Linear Regression with p-value and r^2 =====')
for feature in reg_feature:
    x = summary['frequency']
    y = summary[feature]
    lin_reg = stats.linregress(x, y)
    print('linear_reg ' + feature + ' p-value = ' + str(lin_reg.pvalue))
    print('linear_reg ' + feature + ' r^2 = ' + str(lin_reg.rvalue**2))


'''
Polynomial Regression with r^2
'''
print('\n======= Polynomial Regression with r^2 =======')
for feature in reg_feature:
    x = summary['frequency']
    y = summary[feature]
    poly_reg = np.poly1d(np.polyfit(x, y, 3))
    x_axis = np.linspace(x.min(), x.max(), len(x))
    r2 = r2_score(y, poly_reg(x))
    print('poly_reg ' + feature + ' r^2 = ' + str(r2))

    # Plot the polynomial regression for all data points
    plt.figure()
    plt.scatter(x, y)
    plt.plot(x_axis, poly_reg(x_axis), 'r-')
    plt.xlabel('Step Frequency')
    plt.ylabel(feature)
    plt.legend(['Dataset', 'Polynomial Line'])
    plt.title('Polynomial regression for ' + feature + ' vs step frequency')
    plt.savefig('figures_regression/' + 'poly_reg_' + feature + '.jpg')
    plt.close()