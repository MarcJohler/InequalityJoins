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
from classes import naive_ineqjoin_multicond, naive_ineqjoin_lowsel_multicond, ivec_ineqjoin_multicond, jvec_ineqjoin_multicond, flexible_ineqjoin_multicond
from classes import IE_join, IE_pseudo_self_join


test_cases = 5
#np.random.seed(21)

selectivity = np.zeros(test_cases)
naive_time = np.zeros(test_cases)
lowsel_time = np.zeros(test_cases)
flex_time = np.zeros(test_cases)
nl_time = np.zeros(test_cases)
ivec_time = np.zeros(test_cases)
jvec_time = np.zeros(test_cases)
ie_time = np.zeros(test_cases)
ie_ps_time = np.zeros(test_cases)

for i in range(test_cases):
    predicate_len = 2
    
    n1 = 200
    R = np.random.randint(np.random.randint(1, 5), size = (n1, predicate_len)) 
    R = pd.DataFrame(R)
    
    n2 = 200
    S = np.random.randint(np.random.randint(1, 5), size = (n2, predicate_len)) 
    S = pd.DataFrame(S)
    
    #define random operators
    operators = np.random.choice([operator.lt, operator.le, operator.ge, operator.lt], predicate_len)
    
    #tic_nl = time.perf_counter()
    #nl_join_result = nested_loop_ineqjoin(R, S,  [j for j in range(predicate_len)], [j for j in range(predicate_len)], operators)
    #toc_nl = time.perf_counter()
   
    # measur time for flexible approach
    tic_flex = time.perf_counter()
    flex_join_result = flexible_ineqjoin_multicond(R, S,  [j for j in range(predicate_len)], [j for j in range(predicate_len)], operators)
    toc_flex = time.perf_counter()
    
    # measure time for naive approach for low predicate_size
    #tic_l = time.perf_counter()
    #lowsel_join_result = naive_ineqjoin_lowsel_multicond(R, S,  [j for j in range(predicate_len)], [j for j in range(predicate_len)], operators)
    #toc_l = time.perf_counter()
    
    # measure time for naive approach
    tic_n = time.perf_counter()
    naive_join_result = naive_ineqjoin_multicond(R, S,  [j for j in range(predicate_len)], [j for j in range(predicate_len)], operators)
    toc_n = time.perf_counter()
    
    # measure time for naive approach
    #tic_i = time.perf_counter()
    #ivec_join_result = ivec_ineqjoin_multicond(R, S,  [j for j in range(predicate_len)], [j for j in range(predicate_len)], operators)
    #toc_i = time.perf_counter()
    
    # measure time for naive approach
    tic_j = time.perf_counter()
    jvec_join_result = jvec_ineqjoin_multicond(R, S,  [j for j in range(predicate_len)], [j for j in range(predicate_len)], operators)
    toc_j = time.perf_counter()
    
    """
    # IE approaches
    # measure time for naive approach
    tic_ie = time.perf_counter()
    ie_join_result = IE_join(R, S, [j for j in range(predicate_len)], [j for j in range(predicate_len)], operators)
    toc_ie = time.perf_counter()
    
    tic_ps = time.perf_counter()
    ps_join_result = IE_pseudo_self_join(R, S,  [j for j in range(predicate_len)], [j for j in range(predicate_len)], operators)
    toc_ps = time.perf_counter()
    """    
	
    
    # check if results are correct
    #nl_join_set = set(nl_join_result)
    #lowsel_join_set = set(lowsel_join_result)
    naive_join_set = set(naive_join_result)
    flex_join_set = set(flex_join_result)
    #ivec_join_set = set(ivec_join_result)
    jvec_join_set = set(jvec_join_result)
    
    """
    ie_join_set = set(ie_join_result)
    ps_join_set = set(ps_join_result)
    """
    
    
    #assert naive_join_set.issubset(lowsel_join_set)
    #assert naive_join_set.issuperset(lowsel_join_set)
    assert naive_join_set.issubset(flex_join_set)
    assert naive_join_set.issuperset(flex_join_set)
    #assert naive_join_set.issubset(nl_join_set)
    #assert naive_join_set.issuperset(nl_join_set)
    #assert naive_join_set.issubset(ivec_join_set)
    #assert naive_join_set.issuperset(ivec_join_set)
    assert naive_join_set.issubset(jvec_join_set)
    assert naive_join_set.issuperset(jvec_join_set)
    
    """
    assert naive_join_set.issubset(ie_join_set)
    assert naive_join_set.issuperset(ie_join_set)
    assert naive_join_set.issubset(ps_join_set)
    assert naive_join_set.issuperset(ps_join_set)
    """
    
    # save predicate_size
    selectivity[i] = len(flex_join_result) / (n1 * n2)
    
    print("Test case", i)
    print("Time for naive approach:", {toc_n - tic_n})
    naive_time[i] = toc_n - tic_n
    #print("Time for low predicate_size naive approach:", {toc_l - tic_l})
    #lowsel_time[i] = toc_l - tic_l
    print("Time for flexible approach:", {toc_flex - tic_flex})
    flex_time[i] = toc_flex - tic_flex
    #print("Time for nested loop approach:", {toc_nl - tic_nl})
    #nl_time[i] = toc_nl - tic_nl
    #print("Time for ivec approach:", {toc_i - tic_i})
    #ivec_time[i] = toc_i - tic_i
    print("Time for jvec approach:", {toc_j - tic_j})
    jvec_time[i] = toc_j - tic_j
    
    """
    print("Time for ie approach:", {toc_ie - tic_ie})
    ie_time[i] = toc_ie - tic_ie
    
    print("Time for pseudo self join approach:", {toc_ps - tic_ps})
    ie_ps_time[i] = toc_ps - tic_ps
    """
    
# It is clear that the naive approach performs better than IEJoin
fig, ax = plt.subplots()
plt.scatter(selectivity, naive_time, label = "Naive Approach")
#plt.scatter(selectivity, lowsel_time, label = "Approach for low predicate_size")
plt.scatter(selectivity, flex_time, label = "Flexible Approach")
#plt.scatter(selectivity, nl_time, label = "Nested Loop")
#plt.scatter(selectivity, ivec_time, label = "ivec Approach")
plt.scatter(selectivity, jvec_time, label = "jvec Approach")
"""
plt.scatter(selectivity, ie_time, label = "IEJoin")
plt.scatter(selectivity, ie_ps_time, label = "Pseudo Self Join")
"""
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