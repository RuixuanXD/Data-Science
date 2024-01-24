# 353-project

# Before running:
Before trying to run the python programs, ensure that following libraries/packages are installed:
1) NumPy
2) Pandas
3) Matplotlib
4) Seaborn
5) Scikit-learn
6) Scipy
7) os
8) fnmatch

All collected data is saved in dataset folder, before running, make sure these folders are created: figures_analysis, figures_data, figures_regression. Also, make sure summary.csv, flat.csv, upstairs.csv, and downstairs.csv in the dataset folder are created and filled in with testers' information.

# Running prograss:

**First run the dataProcessing.py**

    python3 dataProcessing.py

This will generate the step frequencies in 4 .csv files (summary, flat, upstairs, and downstairs) in the dataset folder, and output the figures of data at fiures_data folder, which convert the csv file into images.

The other 3 .py file can run in any order after running the dataProcessing.py.

**running command for analysis.py**
    
    python3 analysis.py

This will output figures at figures_analysis folder, and print p-value of ANONA for 2 gender groups.

**running command for classification.py**

    python3 classification.py

This will print the testing scores by using different classification models.

**running command for regression.py**

    python3 regression.py

This will output the figures at figures_regression folder, and print the score of various regression models.