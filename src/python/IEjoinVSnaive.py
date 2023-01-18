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
from classes import naive_ineqjoin_multicond, IE_join, nested_loop_ineqjoin

test_cases = 5
np.random.seed(1)

selectivity = np.zeros(test_cases)
naive_time = np.zeros(test_cases)
ie_time = np.zeros(test_cases)
nl_time = np.zeros(test_cases)

# run this for comparison with constant relation sizes and variable selectivities
for i in range(test_cases):
    n1 = 600
    duration1 = np.random.randint(5, size = n1)
    cost1 = np.random.randint(1000, size = n1)
    R = {'duration':duration1, 'cost':cost1}
    R = pd.DataFrame(R)
    
    n2 = 600
    duration2 = np.random.randint(1000, size = n2)
    cost2 = np.random.randint(5, size = n2)
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
    
    """
    # measure time for ie approach
    tic_nl = time.perf_counter()
    nl_join_result = nested_loop_ineqjoin(R, S,  ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])
    toc_nl = time.perf_counter()
    """
    
    # check if results are correct
    naive_join_set = set(naive_join_result)
    ie_join_set = set(ie_join_result)
    #nl_join_set = set(nl_join_result)
    
    assert naive_join_set.issubset(ie_join_set)
    assert naive_join_set.issuperset(ie_join_set)
    #assert naive_join_set.issubset(nl_join_set)
    #assert naive_join_set.issuperset(nl_join_set)
    
    # save selectivity
    selectivity[i] = len(naive_join_set) / (n1 * n2)
    
    print("Test case", i)
    print("Time for naive approach:", {toc_n - tic_n})
    naive_time[i] = toc_n - tic_n
    print("Time for ie approach:", {toc_ie - tic_ie})
    ie_time[i] = toc_ie - tic_ie
    #print("Time for nested loop approach:", {toc_nl - tic_nl})
    #nl_time[i] = toc_nl - tic_nl
    

# It is clear that the naive approach performs better than IEJoin
fig, ax = plt.subplots()
plt.scatter(selectivity, naive_time, label = "Naive Approach")
plt.scatter(selectivity, ie_time, label = "IEJoin")
#plt.scatter(selectivity, nl_time, label = "Nested Loop")
ax.legend()
plt.show()

"""
# run this for investigation of the relation size
n_sizes = 12
sizes = [(i + 1) * 50 for i in range(n_sizes)]

naive_timeVSsize = np.zeros(n_sizes)
ie_timeVSsize = np.zeros(n_sizes)
nl_timeVSsize = np.zeros(n_sizes)

for i in range(len(sizes)):
    n1 = sizes[i]
    duration1 = np.random.randint(100, size = n1)
    cost1 = np.random.randint(100, size = n1)
    R = {'duration':duration1, 'cost':cost1}
    R = pd.DataFrame(R)
    
    n2 = sizes[i]
    duration2 = np.random.randint(100, size = n2)
    cost2 = np.random.randint(100, size = n2)
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
    
    # measure time for ie approach
    tic_nl = time.perf_counter()
    nl_join_result = nested_loop_ineqjoin(R, S,  ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])
    toc_nl = time.perf_counter()
    
    # check if results are correct
    naive_join_set = set(naive_join_result)
    ie_join_set = set(ie_join_result)
    nl_join_set = set(nl_join_result)
    
    assert naive_join_set.issubset(ie_join_set)
    assert naive_join_set.issuperset(ie_join_set)
    assert naive_join_set.issubset(nl_join_set)
    assert naive_join_set.issuperset(nl_join_set)
    
    print("Size", sizes[i])
    print("Time for naive approach:", {toc_n - tic_n})
    naive_timeVSsize[i] = toc_n - tic_n
    print("Time for ie approach:", {toc_ie - tic_ie})
    ie_timeVSsize[i] = toc_ie - tic_ie
    print("Time for nested loop approach:", {toc_nl - tic_nl})
    nl_timeVSsize[i] = toc_nl - tic_nl

# It is clear that the naive approach performs better than IEJoin
fig, ax = plt.subplots()
plt.scatter(sizes, naive_timeVSsize, label = "Naive Approach")
plt.scatter(sizes, ie_timeVSsize, label = "IEJoin")
plt.scatter(sizes, nl_timeVSsize, label = "Nested Loop")
ax.legend()
plt.show()
"""