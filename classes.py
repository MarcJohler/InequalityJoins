# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 00:47:57 2022

@author: Marc Johler
"""
import numpy as np
import operator

# computes all pairs of the values of two arrays
def pairs(arr1, arr2):
    output = []
    for i in range(len(arr1)):
        for j in range(len(arr2)):
           output.append((arr1[i], arr2[j]))
    return output
    

def naive_antijoin(R, S, r, s, op):
    # initialize the arrays in the right order
    r_sorted = np.sort(R[r])
    rid = np.argsort(R[r])
    s_sorted = np.sort(S[s])
    sid = np.argsort(S[s])
    if op in [operator.lt, operator.le]:
        r_sorted = r_sorted[::-1]
        rid = rid[::-1]
    elif op in [operator.gt, operator.ge]:
        s_sorted = s_sorted[::-1]
        sid = sid[::-1]
    
    result = []
    max_j = len(sid)
    # check for the inequality constraints
    for i in range(len(r_sorted)):
        j = 0
        while j < len(s_sorted): 
            if op(r_sorted[i], s_sorted[j]):
                result.append(pairs(list(rid[i:]), list(sid[:max_j])[j:]))  
                # remember the indices from the second relation
                s_sorted = s_sorted[0:j]
                max_j = j
                break
            j += 1
    return [item for sublist in result for item in sublist]

def naive_antijoin_multicond(R, S, r, s, op):
    # check if the arguments are consistent
    condition_len = len(op)
    assert len(s) == condition_len
    assert len(r) == condition_len
    # for each join condition check the valid tuples
    results = np.repeat(None, condition_len)
    for i in range(condition_len):
        results[i] = naive_antijoin(R, S, r[i], s[i], op[i])
    # only consider tuples which fulfill every join condition
    for i in range(condition_len - 1):
        results[i + 1] = set(results[i]).intersection(set(results[i + 1]))
    
    return list(results[-1])