import pandas as pd
totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

print('City with lowest total precipitation: ')
total_pre = pd.DataFrame(totals).sum(axis=1)
lowest_total_pre = total_pre.idxmin()
print(lowest_total_pre)

print('Average precipitation in each month: ')
ave_pre_month = totals.sum(axis=0) / counts.sum(axis=0)
print(ave_pre_month)

print('Average precipitaion in each city: ')
ave_pre_city = totals.sum(axis=1) / counts.sum(axis=1)
print(ave_pre_city)