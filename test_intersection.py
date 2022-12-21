# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 12:58:32 2022

@author: xZoCk
"""

import pandas as pd
import numpy as np
import operator
import time
import matplotlib.pyplot as plt
from classes import naive_ineqjoin_multicond, naive_ineqjoin_multicond_OLD

test_cases = 100
#np.random.seed(21)

selectivity = np.zeros(test_cases)
new_time = np.zeros(test_cases)
old_time = np.zeros(test_cases)


for i in range(test_cases):
    n1 = 900
    duration1 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n1)
    cost1 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n1)
    value1 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n1)
    val1 = np.random.randint(int(np.random.randint(1, 5, size = 1)), size = n1)
    R = {'duration':duration1, 'cost':cost1, 'value':value1, 'val':val1}
    R = pd.DataFrame(R)
    
    n2 = 800
    duration2 = np.random.randint(int(np.random.randint(1, 5, size = 1)), size = n2)
    cost2 = np.random.randint(int(np.random.randint(1, 5, size = 1)), size = n2)
    value2 = np.random.randint(int(np.random.randint(1, 5, size = 1)), size = n2)
    val2 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n2)
    S = {'duration':duration2, 'cost':cost2, 'value':value2, 'val':val2}
    S = pd.DataFrame(S)
    
    # measure time for naive approach
    tic_new = time.perf_counter()
    new_join_result = naive_ineqjoin_multicond(R, S,  ["duration", "cost", "value", "val"], 
                                                 ["duration", "cost", "value", "val"], [operator.gt, operator.gt, operator.gt, operator.gt])
    toc_new = time.perf_counter()
    
    # measure time for naive approach for low selectivity
    tic_old = time.perf_counter()
    old_join_result = naive_ineqjoin_multicond_OLD(R, S,  ["duration", "cost", "value", "val"], 
                                                         ["duration", "cost", "value", "val"], [operator.gt, operator.gt, operator.gt, operator.gt])
    toc_old = time.perf_counter()
    
    	
    # check if results are correct
    new_join_set = set(new_join_result)
    old_join_set = set(old_join_result)
    
    assert new_join_set.issubset(old_join_set)
    assert new_join_set.issuperset(old_join_set)
    
    # save selectivity
    selectivity[i] = len(new_join_set) / (n1 * n2)
    
    print("Test case", i)
    print("Time for new approach:", {toc_new - tic_new})
    new_time[i] = toc_new - tic_new
    print("Time for old approach:", {toc_old - tic_old})
    old_time[i] = toc_old - tic_old
    
    
# It is clear that the naive approach performs better than IEJoin
fig, ax = plt.subplots()
plt.scatter(selectivity, new_time, label = "New intersect")
plt.scatter(selectivity, old_time, label = "Old intersect")
ax.legend()
plt.show()