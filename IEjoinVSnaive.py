# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 11:17:26 2022

@author: MarcJohler
"""

import pandas as pd
import numpy as np
import operator
import time
import matplotlib.pyplot as plt
from classes import naive_ineqjoin_multicond, IE_join

test_cases = 10
np.random.seed(21)

selectivity = np.zeros(test_cases)
naive_time = np.zeros(test_cases)
ie_time = np.zeros(test_cases)

for i in range(test_cases):
    n1 = 200
    duration1 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n1)
    cost1 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n1)
    R = {'duration':duration1, 'cost':cost1}
    R = pd.DataFrame(R)
    
    n2 = 300
    duration2 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n2)
    cost2 = np.random.randint(int(np.random.randint(1, 100, size = 1)), size = n2)
    S = {'duration':duration2, 'cost':cost2}
    S = pd.DataFrame(S)
    
    # measure time for naive approach
    tic_n = time.perf_counter()
    naive_join_result = naive_ineqjoin_multicond(R, S, ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])
    toc_n = time.perf_counter()
    
    # measure time for naive approach for low selectivity
    tic_ie = time.perf_counter()
    ie_join_result = IE_join(R, S, ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])
    toc_ie = time.perf_counter()
    
    # check if results are correct
    naive_join_set = set(naive_join_result)
    ie_join_set = set(ie_join_result)
    
    assert naive_join_set.issubset(ie_join_set)
    assert naive_join_set.issuperset(ie_join_set)
    
    # save selectivity
    selectivity[i] = len(naive_join_set) / (n1 * n2)
    
    print("Test case", i)
    print("Time for naive approach:", {toc_n - tic_n})
    naive_time[i] = toc_n - tic_n
    print("Time for ie approach:", {toc_ie - tic_ie})
    ie_time[i] = toc_ie - tic_ie
    

# It is clear that the naive approach performs better than IEJoin
fig, ax = plt.subplots()
plt.scatter(selectivity, naive_time, label = "Naive Approach")
plt.scatter(selectivity, ie_time, label = "IEJoin")
ax.legend()
plt.show()
