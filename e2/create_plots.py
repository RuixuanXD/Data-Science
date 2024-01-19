import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
# python3 create_plots.py pagecounts-20190509-120000.txt pagecounts-20190509-130000.txt

filename1 = sys.argv[1]
filename2 = sys.argv[2]
file1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])
file2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])

sorted_data = file1.sort_values(by='views', ascending=False)
plot1 = sorted_data['views'].values
#print(sorted_data)

plot2 = pd.merge(file1, file2, on='page')

plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.plot(plot1) # build plot 1
plt.title('Popularity Distribution')
plt.xlabel('Rank')
plt.ylabel('Views')

plt.subplot(1, 2, 2) # select the second
plt.scatter(plot2['views_x'], plot2['views_y']) # build plot 2
plt.xscale('log')
plt.yscale('log')
plt.title('Hourly Correlation')
plt.xlabel('Hour 1 views')
plt.ylabel('Hour 2 views')
plt.savefig('wikipedia.png')
#plt.show()