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
from classes import compare_intersection_planners, jvec_smart_ineqjoin_multicond, intersect_results

test_cases = 10
np.random.seed(21)

selectivity = np.zeros(test_cases)
baseline_time = np.zeros(test_cases)
join_time = np.zeros(test_cases)
dicts_lazy_time = np.zeros(test_cases)
dicts_greedy_time = np.zeros(test_cases)
dicts_exhaustive_time = np.zeros(test_cases)
dicts_adaptive_time = np.zeros(test_cases)
dicts_smart_time = np.zeros(test_cases)

for i in range(test_cases):
    predicate_len = 20
    # replace this by a randomly generated list of join dictionaries (result from jvec_smart_ineqjoin_multicond)
    n1 = 1000
    R = np.random.uniform(0, 1, size = (n1, 1))
    for j in range(predicate_len - 1):
        R = np.concatenate([R, np.random.uniform(0, (j + 2), size = (n1, 1))], axis = 1)
    R = pd.DataFrame(R)
    
    # introduce correlation in the dataset
    for j in range(predicate_len - 1):
        R[j + 1] = R[j + 1] - R[j]
    
    n2 = 1000
    S = np.random.uniform(0, 1, size = (n2, 1))
    for j in range(predicate_len - 1):
        S = np.concatenate([S, np.random.uniform((0 - j - 1), 1, size = (n2, 1))], axis = 1)
    S = pd.DataFrame(S)
    
    # introduce correlation in the dataset
    for j in range(predicate_len - 1):
        S[j + 1] = S[j + 1] - S[j]
    
    predicate = [j for j in range(predicate_len)]
    
    operators = np.random.choice([operator.gt, operator.ge], predicate_len)
    
    tic = time.perf_counter()
    results, res_lengths = jvec_smart_ineqjoin_multicond(R, S, predicate , predicate , operators, intersect_strategy = False)
    join_time[i] = time.perf_counter() - tic
    
    #compare_intersection_planners(R, S, predicate, predicate, operators, show_first = 50)
    
    
    dicts_lazy_time[i] = intersect_results(results, res_lengths, "lazy", evaluation_mode = "total")
    dicts_greedy_time[i] = intersect_results(results, res_lengths, "greedy", evaluation_mode = "total")
    #dicts_exhaustive_time[i] = intersect_results(results, res_lengths, "exhaustive", evaluation_mode = "total")
    #dicts_adaptive_time[i] = intersect_results(results, res_lengths, "adaptive", evaluation_mode = "total")
    dicts_smart_time[i] = intersect_results(results, res_lengths, "smart", evaluation_mode = "total")
    
    
    
fig, ax = plt.subplots()
#plt.scatter(range(test_cases), join_time, label = "Join Time")
plt.scatter(range(test_cases), dicts_lazy_time, label = "Lazy Approach - Case Time")
plt.scatter(range(test_cases), dicts_greedy_time, label = "Greedy Approach - Case Time")
#plt.scatter(range(test_cases), dicts_exhaustive_time, label = "Exhaustive Approach - Case Time")
#plt.scatter(range(test_cases), dicts_adaptive_time, label = "Adaptive Approach - Case Time")
plt.scatter(range(test_cases), dicts_smart_time, label = "Smart Approach - Case Time")
ax.legend()
plt.show()