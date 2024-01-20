import sys
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import mannwhitneyu


OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)

# python3 ab_analysis.py searches.json
def main():
    searchdata_file = sys.argv[1]

    # ...
    
    data = pd.read_json(searchdata_file, orient='records', lines=True)
    #print(data)

    odd_uid = data[data['uid'] % 2 != 0]
    even_uid = data[data['uid'] % 2 == 0]
    at_least_onec_odd = odd_uid[odd_uid['search_count'] > 0]
    never_odd = odd_uid[odd_uid['search_count'] == 0]
    at_least_onec_even = even_uid[even_uid['search_count'] > 0]
    never_even = even_uid[even_uid['search_count'] == 0]
    #print(even_uid)
    chi2, MUP, dof, exp = chi2_contingency(np.array([[len(at_least_onec_odd), len(never_odd)], [len(at_least_onec_even), len(never_even)]]))
    MSP = mannwhitneyu(odd_uid['search_count'], even_uid['search_count']).pvalue
    #print(MUP)

    odd_ins = odd_uid[odd_uid['is_instructor'] == True]
    even_ins = even_uid[even_uid['is_instructor'] == True]
    at_least_onec_odd_ins = odd_ins[odd_ins['search_count'] > 0]
    never_odd_ins = odd_ins[odd_ins['search_count'] == 0]
    at_least_onec_even_ins = even_ins[even_ins['search_count'] > 0]
    never_even_ins = even_ins[even_ins['search_count'] == 0]
    c, MIP, d, e = chi2_contingency(np.array([[len(at_least_onec_odd_ins), len(never_odd_ins)], [len(at_least_onec_even_ins), len(never_even_ins)]]))
    MISP = mannwhitneyu(odd_ins['search_count'], even_ins['search_count']).pvalue

    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=MUP,
        more_searches_p=MSP,
        more_instr_p=MIP,
        more_instr_searches_p=MISP,
    ))


if __name__ == '__main__':
    main()

'''
"Did more/less users use the search feature?" p-value:  0.168
"Did users search more/less?" p-value:  0.141 
"Did more/less instructors use the search feature?" p-value:  0.052
"Did instructors search more/less?" p-value:  0.045
'''