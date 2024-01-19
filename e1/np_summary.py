import numpy as np
data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

print('Row with lowest total precipitaion: ')
total_pre = np.sum(totals, axis=1)
lowest_total_pre = np.argmin(total_pre)
print(lowest_total_pre)

print('Average precipitation in each month: ')
ave_pre_month = np.sum(totals, axis=0) / np.sum(counts, axis=0)
print(ave_pre_month)

print('Average precipitaion in each city: ')
ave_pre_city = np.sum(totals, axis=1) / np.sum(counts, axis=1)
print(ave_pre_city)

print('Quarterly precipition totals: ')
quarter_pre = np.reshape(totals, (4*totals.shape[0], 3))
quarter_pre = np.sum(quarter_pre, axis=1)
quarter_pre = np.reshape(quarter_pre, (totals.shape[0],4))
print(quarter_pre)
