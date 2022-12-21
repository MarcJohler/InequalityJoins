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
from classes import naive_ineqjoin_multicond, naive_ineqjoin_lowsel_multicond
from classes import flexible_ineqjoin_multicond, nested_loop_ineqjoin

test_cases = 100
#np.random.seed(21)

selectivity = np.zeros(test_cases)
naive_time = np.zeros(test_cases)
lowsel_time = np.zeros(test_cases)
flex_time = np.zeros(test_cases)
nl_time = np.zeros(test_cases)


for i in range(test_cases):
    n1 = 500
    duration1 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n1)
    cost1 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n1)
    value1 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n1)
    R = {'duration':duration1, 'cost':cost1, 'value':value1}
    R = pd.DataFrame(R)
    
    n2 = 400
    duration2 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n2)
    cost2 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n2)
    value2 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n2)
    S = {'duration':duration2, 'cost':cost2, 'value':value2}
    S = pd.DataFrame(S)
    
    # measure time for naive approach
    tic_n = time.perf_counter()
    naive_join_result = naive_ineqjoin_multicond(R, S,  ["duration", "cost", "value"], 
                                                 ["duration", "cost", "value"], [operator.lt, operator.gt, operator.le])
    toc_n = time.perf_counter()
    
    # measure time for naive approach for low selectivity
    tic_l = time.perf_counter()
    lowsel_join_result = naive_ineqjoin_lowsel_multicond(R, S,  ["duration", "cost", "value"], 
                                                         ["duration", "cost", "value"], [operator.lt, operator.gt, operator.le])
    toc_l = time.perf_counter()
    
    # measure time for ie approach
    tic_flex = time.perf_counter()
    flex_join_result = flexible_ineqjoin_multicond(R, S,  ["duration", "cost", "value"], 
                                                   ["duration", "cost", "value"], [operator.lt, operator.gt, operator.le])
    toc_flex = time.perf_counter()
    
    # measure time for ie approach
    tic_nl = time.perf_counter()
    nl_join_result = nested_loop_ineqjoin(R, S,  ["duration", "cost", "value"], 
                                                   ["duration", "cost", "value"], [operator.lt, operator.gt, operator.le])
    toc_nl = time.perf_counter()
    	
    # check if results are correct
    naive_join_set = set(naive_join_result)
    lowsel_join_set = set(lowsel_join_result)
    flex_join_set = set(flex_join_result)
    nl_join_set = set(nl_join_result)
    
    assert naive_join_set.issubset(lowsel_join_set)
    assert naive_join_set.issuperset(lowsel_join_set)
    assert naive_join_set.issubset(flex_join_set)
    assert naive_join_set.issuperset(flex_join_set)
    assert naive_join_set.issubset(nl_join_set)
    assert naive_join_set.issuperset(nl_join_set)
    
    # save selectivity
    selectivity[i] = len(naive_join_set) / (n1 * n2)
    
    print("Test case", i)
    print("Time for naive approach:", {toc_n - tic_n})
    naive_time[i] = toc_n - tic_n
    print("Time for low selectivity naive approach:", {toc_l - tic_l})
    lowsel_time[i] = toc_l - tic_l
    print("Time for flexible approach:", {toc_flex - tic_flex})
    flex_time[i] = toc_flex - tic_flex
    print("Time for nested loop approach:", {toc_nl - tic_nl})
    nl_time[i] = toc_nl - tic_nl
    
# It is clear that the naive approach performs better than IEJoin
fig, ax = plt.subplots()
plt.scatter(selectivity, naive_time, label = "Naive Approach")
plt.scatter(selectivity, lowsel_time, label = "Approach for low selectivity")
plt.scatter(selectivity, flex_time, label = "Flexible Approach")
plt.scatter(selectivity, nl_time, label = "Nested Loop")
ax.legend()
plt.show()