import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn
seaborn.set()

data = pd.read_csv('dataset/summary.csv')
flat = pd.read_csv('dataset/flat/flat.csv')
upstairs = pd.read_csv('dataset/upstairs/upstairs.csv')
downstairs = pd.read_csv('dataset/downstairs/downstairs.csv')

data_freq = data['frequency']
flat_freq = flat['frequency']
up_freq = upstairs['frequency']
down_freq = downstairs['frequency']


# def mann_whitney_u():
#     """
#     Mann–Whitney U test for flat, upstairs, and downstairs data
#     :return: none
#     """
#     flat_up = stats.mannwhitneyu(flat_freq, up_freq).pvalue
#     flat_down = stats.mannwhitneyu(flat_freq, down_freq).pvalue
#     up_down = stats.mannwhitneyu(up_freq, down_freq).pvalue
#     print('===== Mann–Whitney U test =====')
#     print('flat vs upstairs p-value = ', flat_up)
#     print('flat vs downstairs p-value = ', flat_down)
#     print('upstairs vs downstairs p-value = ', up_down)


def plot_walk_type():
    """
    Plot histogram of step frequency vs walking types
    :return: none
    """
    bin_size = 10
    x_range = [0.6, 2.1]
    plt.figure()
    plt.hist(flat_freq, bins=bin_size, range=x_range, label='flat')
    plt.hist(up_freq, bins=bin_size, range=x_range, label='upstairs')
    plt.hist(down_freq, bins=bin_size, range=x_range, label='downstairs')
    plt.title('Step frequencies vs Walking types')
    plt.ylabel('Count')
    plt.xlabel('Step frequency')
    plt.legend()
    plt.savefig('figures_analysis/walk_type_hist.jpg')
    plt.close()


def plot_step_freq():
    """
    Plot distribution of step frequencies for all data of flat ground
    :return: none
    """
    plt.figure()
    plt.hist(data_freq, bins=15)
    plt.title('Distribution of step frequencies for flat ground')
    plt.ylabel('Count')
    plt.xlabel('Step frequency')
    plt.savefig('figures_analysis/step_freq_hist.jpg')
    plt.close()


def plot_gender_percent():
    """
    Plot pie chart of percentage of gender for all testers
    :return: none
    """
    plt.figure()
    gender_group = data.groupby('gender').aggregate('count')
    plt.pie(gender_group['name'], labels=['female', 'male'], autopct='%.1f%%')
    plt.title('Percentage of Males vs Females')
    plt.savefig('figures_analysis/gender_pie.jpg')
    plt.close()

def plot_gender_step_freq(female, male):
    plt.figure()
    plt.hist(male['frequency'], color='r', label='male')
    plt.hist(female['frequency'], color='b', label='female')
    plt.xlabel("Step Frequency")
    plt.ylabel("Count")
    plt.title("Distribution of step frequencies for female and male")
    plt.legend()
    plt.savefig('figures_analysis/gender_freq.jpg')
    plt.close()


def main():
    # mann_whitney_u()
    plot_walk_type()
    plot_step_freq()
    plot_gender_percent()

    gender_group = data.groupby('gender').mean(numeric_only=True)
    print(gender_group)

    female = data[data['gender'] == 'f']
    male = data[data['gender'] == 'm']
    anova = stats.f_oneway(female['frequency'], male['frequency'])
    print('\np-value of ANONA for two gender groups is', anova.pvalue)

    plot_gender_step_freq(female, male)

    

if __name__ == '__main__':
    main()
