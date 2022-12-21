# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 13:50:31 2022

@author: Marc Johler
"""

import pandas as pd
import numpy as np
import operator
import time
import matplotlib.pyplot as plt
from classes import naive_ineqjoin_multicond, naive_ineqjoin_lowsel_multicond, flexible_ineqjoin_multicond

test_cases = 100
#np.random.seed(21)

selectivity = np.zeros(test_cases)
naive_time = np.zeros(test_cases)
lowsel_time = np.zeros(test_cases)
flex_time = np.zeros(test_cases)


for i in range(test_cases):
    n1 = 1000
    duration1 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n1)
    cost1 = np.random.randint(int(np.random.randint(1, 5, size = 1)), size = n1)
    R = {'duration':duration1, 'cost':cost1}
    R = pd.DataFrame(R)
    
    n2 = 900
    duration2 = np.random.randint(int(np.random.randint(1, 10, size = 1)), size = n2)
    cost2 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n2)
    S = {'duration':duration2, 'cost':cost2}
    S = pd.DataFrame(S)
    
    # measure time for naive approach
    tic_n = time.perf_counter()
    naive_join_result = naive_ineqjoin_multicond(R, S, ["duration"], ["duration"], [operator.lt])
    toc_n = time.perf_counter()
    
    # measure time for naive approach for low selectivity
    tic_l = time.perf_counter()
    lowsel_join_result = naive_ineqjoin_lowsel_multicond(R, S, ["duration"], ["duration"], [operator.lt])
    toc_l = time.perf_counter()
    
    # measure time for ie approach
    tic_flex = time.perf_counter()
    flex_join_result = flexible_ineqjoin_multicond(R, S, ["duration"], ["duration"], [operator.lt])
    toc_flex = time.perf_counter()
    	
    # check if results are correct
    naive_join_set = set(naive_join_result)
    lowsel_join_result = set(lowsel_join_result)
    flex_join_set = set(flex_join_result)
    
    assert naive_join_set.issubset(lowsel_join_result)
    assert naive_join_set.issuperset(lowsel_join_result)
    assert naive_join_set.issubset(flex_join_result)
    assert naive_join_set.issuperset(flex_join_result)
    
    # save selectivity
    selectivity[i] = len(naive_join_set) / (n1 * n2)
    
    print("Test case", i)
    print("Time for naive approach:", {toc_n - tic_n})
    naive_time[i] = toc_n - tic_n
    print("Time for low selectivity naive approach:", {toc_l - tic_l})
    lowsel_time[i] = toc_l - tic_l
    print("Time for flexible approach:", {toc_flex - tic_flex})
    flex_time[i] = toc_flex - tic_flex
    
# It is clear that the naive approach performs better than IEJoin
fig, ax = plt.subplots()
plt.scatter(selectivity, naive_time, label = "Naive Approach")
plt.scatter(selectivity, lowsel_time, label = "Approach for low selectivity")
plt.scatter(selectivity, flex_time, label = "Flexible Approach")
ax.legend()
plt.show()