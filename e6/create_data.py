import time
import pandas as pd
import numpy as np
from implementations import all_implementations

# time python3 create_data.py # just check the time
# timeout -s SIGKILL 60 python3 create_data.py # kill after 60 seconds

data = pd.DataFrame(np.zeros((100,7), dtype=float), columns=['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort'])

for i in range(100):
    array = []
    for sort in all_implementations:
        random_array = np.random.randint(-10000, 10000, size=20000)
        st = time.time()
        res = sort(random_array)
        en = time.time()
        array.append(en - st)
    data.iloc[i] = array

data.to_csv('data.csv', index=False)