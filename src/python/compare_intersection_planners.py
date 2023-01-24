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
from classes import compare_intersection_planners

test_cases = 1
#np.random.seed(21)

selectivity = np.zeros(test_cases)
baseline_time = np.zeros(test_cases)
dicts_lazy_time = np.zeros(test_cases)
dicts_greedy_time = np.zeros(test_cases)
dicts_exhaustive_time = np.zeros(test_cases)

for i in range(test_cases):
    predicate_len = 50
    n1 = 1000
    R = np.random.uniform(0, np.random.uniform((test_cases - i) / test_cases, 1), size = (n1, 1))
    for j in range(predicate_len - 1):
        R = np.concatenate([R, np.random.uniform(0,  np.random.uniform((test_cases - i) / test_cases, 1), size = (n1, 1))], axis = 1)
    R = pd.DataFrame(R)
    
    # introduce correlation in the dataset
    for j in range(predicate_len - 1):
        R[j + 1] = R[j + 1] - R[j]
    
    n2 = 1000
    S = np.random.uniform(0, np.random.uniform((i + 1) / test_cases, 1), size = (n2, 1))
    for j in range(predicate_len - 1):
        S = np.concatenate([S, np.random.uniform(0, np.random.uniform((i + 1) / test_cases, 1), size = (n2, 1))], axis = 1)
    S = pd.DataFrame(S)
    
    # introduce correlation in the dataset
    for j in range(predicate_len - 1):
        S[j + 1] = S[j + 1] - S[j]
    
    predicate = [j for j in range(predicate_len)]
    
    operators = np.random.choice([operator.lt, operator.le], predicate_len)
    
    res = compare_intersection_planners(R, S, predicate, predicate, operators, show_first=30)
    
