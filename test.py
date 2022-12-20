# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 13:50:31 2022

@author: Marc Johler
"""

import pandas as pd
import numpy as np
import operator
from classes import naive_antijoin_multicond, IE_join


test_cases = 20
np.random.seed(42)


for i in range(test_cases):
    n1 = 20
    duration1 = np.random.randint(10, size = n1)
    cost1 = np.random.randint(10, size = n1)
    R = {'duration':duration1, 'cost':cost1}
    R = pd.DataFrame(R)
    
    n2 = 20
    duration2 = np.random.randint(10, size = n2)
    cost2 = np.random.randint(10, size = n2)
    S = {'duration':duration2, 'cost':cost2}
    S = pd.DataFrame(S)
    
    naive_join_result = naive_antijoin_multicond(R, S, ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])
    ie_join_result = IE_join(R, S, ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])

    naive_join_set = set(naive_join_result)
    ie_join_set = set(ie_join_result)
    
    assert naive_join_set.issubset(ie_join_set)
    assert naive_join_set.issuperset(ie_join_set)