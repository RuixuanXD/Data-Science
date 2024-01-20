import sys
import pandas as pd
import numpy as np
import datetime as dt
from scipy import stats
import matplotlib.pyplot as plt


OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)


def main():
    reddit_counts = sys.argv[1]
    counts = pd.read_json(reddit_counts, lines=True)
    counts = counts[((counts['date'].dt.year == 2012) | (counts['date'].dt.year == 2013)) & (counts['subreddit'] == 'canada')]

    weekends = counts[(counts['date'].dt.weekday >= 5)]
    weekdays = counts[(counts['date'].dt.weekday < 5)]
    
    # T-test
    ttest_p = stats.ttest_ind(weekends['comment_count'],weekdays['comment_count']).pvalue
    weekday_normality_p = stats.normaltest(weekdays['comment_count']).pvalue
    weekend_normality_p = stats.normaltest(weekends['comment_count']).pvalue
    levene_p = stats.levene(weekends['comment_count'], weekdays['comment_count']).pvalue
    
    #Fix 1 : Transforming data    
    #use sqrt() to transform the data since thats when the data comes closes to normal distribution
    trans_end = np.log(weekends['comment_count'])
    transformed_weekday = np.log(weekdays['comment_count'])
    transformed_weekend_normality_p = stats.normaltest(trans_end).pvalue
    transformed_weekday_normality_p = stats.normaltest(transformed_weekday).pvalue
    transformed_levene_p = stats.levene(trans_end,transformed_weekday).pvalue
    
    #Fix 2 : Central Limit Theorem
    weekends_iso = weekends['date'].dt.isocalendar()
    weekends_iso = weekends_iso[['year','week']]
    weekends = pd.concat([weekends,weekends_iso], axis=1)
    weekdays_iso = weekdays['date'].dt.isocalendar()
    weekdays_iso = weekdays_iso[['year','week']]
    weekdays = pd.concat([weekdays,weekdays_iso], axis=1)
    
    group_weekend = weekends.groupby(by=['year','week']).aggregate({'comment_count': 'mean'}).reset_index()
    group_weekday = weekdays.groupby(by=['year','week']).aggregate({'comment_count': 'mean'}).reset_index()
    weekly_weekday_normality_p = stats.normaltest(group_weekday['comment_count']).pvalue
    weekly_weekend_normality_p = stats.normaltest(group_weekend['comment_count']).pvalue
    weekly_levene_p = stats.levene(group_weekend['comment_count'],group_weekday['comment_count']).pvalue  
    weekly_ttest_p = stats.ttest_ind(group_weekend['comment_count'],group_weekday['comment_count']).pvalue
    
    #Fix 3 : Non-parametric test
    utest_p = stats.mannwhitneyu(weekends['comment_count'],weekdays['comment_count'], alternative='two-sided').pvalue
    
    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p = ttest_p,
        initial_weekday_normality_p = weekday_normality_p,
        initial_weekend_normality_p = weekend_normality_p,
        initial_levene_p = levene_p,
        transformed_weekday_normality_p = transformed_weekday_normality_p,
        transformed_weekend_normality_p = transformed_weekend_normality_p,
        transformed_levene_p = transformed_levene_p,
        weekly_weekday_normality_p = weekly_weekday_normality_p,
        weekly_weekend_normality_p = weekly_weekend_normality_p,
        weekly_levene_p = weekly_levene_p,
        weekly_ttest_p = weekly_ttest_p,
        utest_p = utest_p,
    ))


if __name__ == '__main__':
    main()
