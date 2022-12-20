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
    
# computes the antijoin with one join predicates
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

# computes the antijoin with multiple join predicates
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

# computes the permutation array for the IE Join
def compute_permutation_array(arr1, arr2):
    assert len(arr1) == len(arr2)
    perm_arr = np.zeros(len(arr1))
    for i in range(len(arr2)):
        perm_arr[i] = np.where(arr1 == arr2[i])
    return perm_arr

# computes the IE_join with two join predicates
def IE_join(R, S, r, s, op):
    # check if there are two join predicates
    assert len(op) == 2
    assert len(s) == 2
    assert len(r) == 2
    # extract the respective columns
    r0_sorted = np.sort(R[r[0]])
    rid0 = np.argsort(R[r[0]])
    r1_sorted = np.sort(R[r[1]])
    rid1 = np.argsort(R[r[1]])
    s0_sorted = np.sort(S[s[0]])
    sid0 = np.argsort(S[s[0]])
    s1_sorted = np.sort(S[s[1]])
    sid1 = np.argsort(S[s[1]])
    # sort according to the operator
    """
    sort r0 and s0 in a way that the tuples which are most likely to be on the 
    right-handside of the join condition are right in the order (predicate 0) has
    priority
    
    sort r1 and s1 in the following way:
        if op[1] in [<, <=]:
            descending w.r.t. to 1
        else:
            ascending w.r.t. to 1
    and in case of ties:
        if op[0] in [<, <=]:
            ascending w.r.t. to 0
        else:
            descending w.r.t. to 0
    
    
    if op[0] in [operator.gt, operator.ge]:
        r0_sorted = r0_sorted[::-1]
        rid0 = rid0[::-1]
        s0_sorted = s0_sorted[::-1]
        sid0 = sid0[::-1]
    if op[1] in [operator.lt, operator.le]:
        r1_sorted = r1_sorted[::-1]
        rid1 = rid1[::-1]
        s1_sorted = s1_sorted[::-1]
        sid1 = sid1[::-1]
    
    # compute the permutation arrays
    p_r = compute_permutation_array(rid1, rid0)
    p_s = compute_permutation_array(sid1, sid0)
    
    
    