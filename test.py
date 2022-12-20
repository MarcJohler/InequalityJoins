# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 13:50:31 2022

@author: Marc Johler
"""

import pandas as pd
import numpy as np
import operator
import time
from classes import naive_ineqjoin_multicond, IE_join

test_cases = 5
np.random.seed(21)

for i in range(test_cases):
    n1 = 500
    duration1 = np.random.randint(5, size = n1)
    cost1 = np.random.randint(5, size = n1)
    R = {'duration':duration1, 'cost':cost1}
    R = pd.DataFrame(R)
    
    n2 = 500
    duration2 = np.random.randint(5, size = n2)
    cost2 = np.random.randint(5, size = n2)
    S = {'duration':duration2, 'cost':cost2}
    S = pd.DataFrame(S)
    
    # measure time for naive approach
    tic_n = time.perf_counter()
    naive_join_result = naive_ineqjoin_multicond(R, S, ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])
    toc_n = time.perf_counter()
    
    # measure time for ie approach
    tic_i = time.perf_counter()
    ie_join_result = IE_join(R, S, ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])
    toc_i = time.perf_counter()
    	
    # check if results are correct
    naive_join_set = set(naive_join_result)
    ie_join_set = set(ie_join_result)
    
    assert naive_join_set.issubset(ie_join_set)
    assert naive_join_set.issuperset(ie_join_set)
    
    print("Test case", i)
    print("Time for naive approach:", {toc_n - tic_n})
    print("Time for IE approach:", {toc_i - tic_i})