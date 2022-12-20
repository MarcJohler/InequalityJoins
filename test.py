# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 13:50:31 2022

@author: Marc Johler
"""

import pandas as pd
import numpy as np
import operator
import time
from classes import naive_ineqjoin_multicond, naive_ineqjoin_lowsel_multicond, flexible_ineqjoin_multicond

test_cases = 10
np.random.seed(21)

for i in range(test_cases):
    n1 = 1000
    duration1 = np.random.randint(1000, size = n1)
    cost1 = np.random.randint(1000, size = n1)
    R = {'duration':duration1, 'cost':cost1}
    R = pd.DataFrame(R)
    
    n2 = 1000
    duration2 = np.random.randint(5, size = n2)
    cost2 = np.random.randint(5, size = n2)
    S = {'duration':duration2, 'cost':cost2}
    S = pd.DataFrame(S)
    
    # measure time for naive approach
    tic_n = time.perf_counter()
    naive_join_result = naive_ineqjoin_multicond(R, S, ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])
    toc_n = time.perf_counter()
    
    # measure time for naive approach for low selectivity
    tic_l = time.perf_counter()
    lowsel_join_result = naive_ineqjoin_lowsel_multicond(R, S, ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])
    toc_l = time.perf_counter()
    
    # measure time for ie approach
    tic_flex = time.perf_counter()
    flex_join_result = flexible_ineqjoin_multicond(R, S, ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])
    toc_flex = time.perf_counter()
    	
    # check if results are correct
    naive_join_set = set(naive_join_result)
    lowsel_join_result = set(lowsel_join_result)
    flex_join_set = set(flex_join_result)
    
    assert naive_join_set.issubset(lowsel_join_result)
    assert naive_join_set.issuperset(lowsel_join_result)
    assert naive_join_set.issubset(flex_join_result)
    assert naive_join_set.issuperset(flex_join_result)
    
    print("Test case", i)
    print("Time for naive approach:", {toc_n - tic_n})
    print("Time for low selectivity naive approach:", {toc_l - tic_l})
    print("Time for flexible approach:", {toc_flex - tic_flex})