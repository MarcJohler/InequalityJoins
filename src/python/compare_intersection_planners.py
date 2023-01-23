# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 18:48:08 2023

@author: Marc Johler
"""
import pandas as pd
import numpy as np
import operator
import matplotlib.pyplot as plt
import time
from classes import jvec_ineqjoin_multicond, jvec_smart_ineqjoin_multicond

test_cases = 30
#np.random.seed(21)

selectivity = np.zeros(test_cases)
baseline_time = np.zeros(test_cases)
dicts_lazy_time = np.zeros(test_cases)
dicts_greedy_time = np.zeros(test_cases)
dicts_exhaustive_time = np.zeros(test_cases)

for i in range(test_cases):
    predicate_len = 10
    n1 = 5
    R = np.random.randint(100, size = (n1, predicate_len)) 
    R = pd.DataFrame(R)
    
    n2 = 5
    S = np.random.randint(100, size = (n2, predicate_len)) 
    S = pd.DataFrame(S)
    
    predicate = [j for j in range(predicate_len)]
    
    operators = np.random.choice([operator.lt, operator.le, operator.lt, operator.ge], predicate_len)
    
    # measure time for baseline approach
    tic_base = time.perf_counter()
    baseline_join_result = jvec_ineqjoin_multicond(R, S,  predicate, predicate, operators)
    toc_base = time.perf_counter()
    
    # measure time for lazy strategy with dictionaries
    tic_lazy = time.perf_counter()
    lazy_join_result = jvec_smart_ineqjoin_multicond(R, S,  predicate, predicate, operators, 
                                                     intersect_strategy = "lazy")
    toc_lazy = time.perf_counter()
    
    # measure time for lazy strategy with dictionaries
    tic_greedy = time.perf_counter()
    greedy_join_result = jvec_smart_ineqjoin_multicond(R, S,  predicate, predicate, operators,
                                                       intersect_strategy = "greedy")
    toc_greedy = time.perf_counter()
    
    # measure time for exhaustive strategy with dictionaries
    tic_exhaustive = time.perf_counter()
    exhaustive_join_result = jvec_smart_ineqjoin_multicond(R, S,  predicate, predicate, operators,
                                                           intersect_strategy = "exhaustive")
    toc_exhaustive = time.perf_counter()
    
    
    baseline_set = set(baseline_join_result)
    lazy_set = set(lazy_join_result)
    greedy_set = set(greedy_join_result)
    exhaustive_set = set(exhaustive_join_result)
    
    assert baseline_set.issubset(lazy_set)
    assert baseline_set.issuperset(lazy_set)
    assert baseline_set.issubset(greedy_set)
    assert baseline_set.issuperset(greedy_set)
    assert baseline_set.issubset(exhaustive_set)
    assert baseline_set.issuperset(exhaustive_set)
        
    
    print("Test case", i)
    print("Time for baseline approach:", {toc_base - tic_base})
    baseline_time[i] = toc_base - tic_base
    print("Time for lazy approach:", {toc_lazy - tic_lazy})
    dicts_lazy_time[i] = toc_lazy - tic_lazy
    print("Time for greedy approach:", {toc_greedy - tic_greedy})
    dicts_greedy_time[i] = toc_greedy - tic_greedy
    print("Time for exhaustive approach:", {toc_exhaustive - tic_exhaustive})
    dicts_exhaustive_time[i] = toc_exhaustive - tic_exhaustive
  

fig, ax = plt.subplots()
plt.scatter(range(test_cases), baseline_time, label = "Baseline Approach")
plt.scatter(range(test_cases), dicts_lazy_time, label = "Lazy Approach")
plt.scatter(range(test_cases), dicts_greedy_time, label = "Greedy Approach")
plt.scatter(range(test_cases), dicts_exhaustive_time, label = "Exhaustive Approach")
ax.legend()
plt.show()
