import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv('data.csv')

anova = stats.f_oneway(data['qs1'], data['qs2'], data['qs3'], data['qs4'], data['qs5'], data['merge1'], data['partition_sort'])
#print(anova)
print("ANOVA p-value = ", anova.pvalue)

x_melt = pd.melt(data)
posthoc = pairwise_tukeyhsd(x_melt['value'], x_melt['variable'], alpha=0.05)

fig = posthoc.plot_simultaneous()

print('Ranking speed')
print('Algorithm         Mean')
information = data.describe()
print(information.loc['mean'].sort_values().to_string())

