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
from classes import flexible_ineqjoin_multicond, nested_loop_ineqjoin, efficient_ineqjoin_multicond

test_cases = 10
np.random.seed(21)

predicate_size = np.zeros(test_cases)
naive_time = np.zeros(test_cases)
lowsel_time = np.zeros(test_cases)
flex_time = np.zeros(test_cases)
nl_time = np.zeros(test_cases)
efficient_time = np.zeros(test_cases)


for i in range(test_cases):
    n1 = 1000
    R = np.random.randint(100, size = (n1, i + 1)) 
    R = pd.DataFrame(R)
    
    n2 = 1000
    S = np.random.randint(5, size = (n2, i + 1)) 
    S = pd.DataFrame(S)
    
    #define random operators
    operators = np.random.choice([operator.lt, operator.gt, operator.le, operator.ge], i + 1)
    
    """
    # measure time for ie approach
    tic_nl = time.perf_counter()
    nl_join_result = nested_loop_ineqjoin(R, S,  [j for j in range(i + 1)], [j for j in range(i + 1)], operators)
    toc_nl = time.perf_counter()
    
    # measure time for naive approach for low predicate_size
    tic_l = time.perf_counter()
    lowsel_join_result = naive_ineqjoin_lowsel_multicond(R, S,  [j for j in range(i + 1)], [j for j in range(i + 1)], operators)
    toc_l = time.perf_counter()
    """
    # measure time for ie approach
    tic_flex = time.perf_counter()
    flex_join_result = flexible_ineqjoin_multicond(R, S,  [j for j in range(i + 1)], [j for j in range(i + 1)], operators)
    toc_flex = time.perf_counter()
    
    # measure time for naive approach
    tic_n = time.perf_counter()
    naive_join_result = naive_ineqjoin_multicond(R, S,  [j for j in range(i + 1)], [j for j in range(i + 1)], operators)
    toc_n = time.perf_counter()
    
    # measure time for naive approach
    tic_e = time.perf_counter()
    efficient_join_result = efficient_ineqjoin_multicond(R, S,  [j for j in range(i + 1)], [j for j in range(i + 1)], operators)
    toc_e = time.perf_counter()
    	
    # check if results are correct
    #nl_join_set = set(nl_join_result)
    #lowsel_join_set = set(lowsel_join_result)
    naive_join_set = set(naive_join_result)
    flex_join_set = set(flex_join_result)
    efficient_join_set = set(efficient_join_result)
    
    #assert naive_join_set.issubset(lowsel_join_set)
    #assert naive_join_set.issuperset(lowsel_join_set)
    assert naive_join_set.issubset(flex_join_set)
    assert naive_join_set.issuperset(flex_join_set)
    #assert naive_join_set.issubset(nl_join_set)
    #assert naive_join_set.issuperset(nl_join_set)
    assert naive_join_set.issubset(efficient_join_set)
    assert naive_join_set.issuperset(efficient_join_set)
    
    # save predicate_size
    predicate_size[i] = i
    
    print("Test case", i)
    print("Time for naive approach:", {toc_n - tic_n})
    naive_time[i] = toc_n - tic_n
    #print("Time for low predicate_size naive approach:", {toc_l - tic_l})
    #lowsel_time[i] = toc_l - tic_l
    print("Time for flexible approach:", {toc_flex - tic_flex})
    flex_time[i] = toc_flex - tic_flex
    #print("Time for nested loop approach:", {toc_nl - tic_nl})
    #nl_time[i] = toc_nl - tic_nl
    print("Time for efficient approach:", {toc_e - tic_e})
    efficient_time[i] = toc_e - tic_e
    
# It is clear that the naive approach performs better than IEJoin
fig, ax = plt.subplots()
plt.scatter(predicate_size, naive_time, label = "Naive Approach")
#plt.scatter(predicate_size, lowsel_time, label = "Approach for low predicate_size")
plt.scatter(predicate_size, flex_time, label = "Flexible Approach")
#plt.scatter(predicate_size, nl_time, label = "Nested Loop")
plt.scatter(predicate_size, efficient_time, label = "Efficient Approach")
ax.legend()
plt.show()