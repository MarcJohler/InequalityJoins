# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 12:05:13 2023

@author: Marc Johler
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 01:28:51 2022

@author: Marc Johler
"""

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
from classes import IE_self_join, naive_selfjoin_multicond


test_cases = 20
np.random.seed(21)

selectivity = np.zeros(test_cases)
naive_time = np.zeros(test_cases)
ie_time = np.zeros(test_cases)

for i in range(test_cases):
    predicate_len = 2
    
    n = 100
    R = np.random.randint(np.random.randint(1, 5), size = (n, predicate_len)) 
    R = pd.DataFrame(R)
    
    #define random operators
    operators = np.random.choice([operator.ge, operator.ge], predicate_len)
   
    # measur time for flexible approach
    tic_ie = time.perf_counter()
    ie_join_result = IE_self_join(R, [j for j in range(predicate_len)], operators)
    toc_ie = time.perf_counter()
    
    # measure time for naive approach
    tic_n = time.perf_counter()
    naive_join_result = naive_selfjoin_multicond(R, [j for j in range(predicate_len)], operators)
    toc_n = time.perf_counter()
 
    naive_join_set = set(naive_join_result)
    ie_join_set = set(ie_join_result)
    
    # save predicate_size
    selectivity[i] = len(naive_join_result) / (n**2)
    
    assert naive_join_set.issubset(ie_join_set)
    assert naive_join_set.issuperset(ie_join_set)
    
    print("Test case", i)
    print("Time for naive approach:", {toc_n - tic_n})
    naive_time[i] = toc_n - tic_n
    print("Time for ie approach:", {toc_ie - tic_ie})
    ie_time[i] = toc_ie - tic_ie
    
# It is clear that the naive approach performs better than IEJoin
fig, ax = plt.subplots()
plt.scatter(selectivity, naive_time, label = "Naive Approach")
plt.scatter(selectivity, ie_time, label = "IE SelfJoin")
ax.legend()
plt.show()


"""
# run this for investigation of the relation size
n_sizes = 10
sizes = [(i + 1) * 200 for i in range(n_sizes)]

naive_time = np.zeros(n_sizes)
jvec_time = np.zeros(n_sizes)

for i in range(len(sizes)):
    predicate_len = 1
    n1 = sizes[i]
    R = np.random.randint(100, size = (n1, predicate_len)) 
    R = pd.DataFrame(R)
    
    n2 = sizes[i]
    S = np.random.randint(100, size = (n2, predicate_len)) 
    S = pd.DataFrame(S)
    
    #define random operators
    operators = np.random.choice([operator.lt, operator.le], predicate_len)
    
    # measure time for naive approach
    tic_n = time.perf_counter()
    naive_join_result = naive_ineqjoin_multicond(R, S,  [j for j in range(predicate_len)], [j for j in range(predicate_len)], operators)
    toc_n = time.perf_counter()
    
    # measure time for naive approach
    tic_j = time.perf_counter()
    jvec_join_result = jvec_ineqjoin_multicond(R, S,  [j for j in range(predicate_len)], [j for j in range(predicate_len)], operators)
    toc_j = time.perf_counter()
    
    # check if results are correct
    naive_join_set = set(naive_join_result)
    jvec_join_set = set(jvec_join_result)
    
    assert naive_join_set.issubset(jvec_join_set)
    assert naive_join_set.issuperset(jvec_join_set)
    
    print("Size", sizes[i])
    print("Time for naive approach:", {toc_n - tic_n})
    naive_time[i] = toc_n - tic_n
    print("Time for jvec approach:", {toc_j - tic_j})
    jvec_time[i] = toc_j - tic_j
    

# It is clear that the naive approach performs better than IEJoin
fig, ax = plt.subplots()
plt.scatter(sizes, naive_time, label = "Naive Approach")
plt.scatter(sizes, jvec_time, label = "Jvec approach")
ax.legend()
plt.show()
"""