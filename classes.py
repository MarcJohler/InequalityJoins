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
    
# computes the antijoin with one join predicate
def naive_ineqjoin(R, S, r, s, op):
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
    # check for the inequality constraints
    for i in range(len(r_sorted)):
        j = 0
        while j < len(s_sorted): 
            if op(r_sorted[i], s_sorted[j]):
                result.append(pairs(list(rid[i:]), list(sid[j:])))  
                # remember the indices from the second relation
                s_sorted = s_sorted[0:j]
                sid = sid[0:j]
                break
            j += 1
    result = [item for sublist in result for item in sublist]
    return result, len(result)

# function for inequality joins with low selectivity
def naive_ineqjoin_lowsel(R, S, r, s, op):
    # initialize the arrays in the right order
    r_sorted = np.sort(R[r])
    rid = np.argsort(R[r])
    s_sorted = np.sort(S[s])
    sid = np.argsort(S[s])
    if op in [operator.lt, operator.le]:
        s_sorted = s_sorted[::-1]
        sid = sid[::-1]
    elif op in [operator.gt, operator.ge]:
        r_sorted = r_sorted[::-1]
        rid = rid[::-1]
        
    result = []
    # check for the inequality constraints
    for i in range(len(r_sorted)):
        j = 0
        while j < len(s_sorted): 
            if op(r_sorted[i], s_sorted[j]):
                result.append((rid[rid.index[i]], sid[sid.index[j]]))  
            else:
                # remember the indices from the second relation
                s_sorted = s_sorted[0:j]
                break
            j += 1
    return result, len(result)

# this should be the most efficient approach
def ivec_ineqjoin(R, S, r, s, op):
    # initialize the arrays in the right order
    r_sorted = np.sort(R[r])
    rid = np.argsort(R[r])
    s_sorted = np.sort(S[s])
    sid = np.argsort(S[s])
    if op in [operator.lt, operator.le]:
        r_sorted = r_sorted[::-1]
        rid = rid[::-1]
        s_sorted = s_sorted[::-1]
        sid = sid[::-1]
    
    result = []
    done = False
    # check for the inequality constraints
    for i in range(len(r_sorted)):
        j = 0
        while j < len(s_sorted): 
            if op(r_sorted[i], s_sorted[j]):
                result.append(pairs(list(rid[i:]), [sid[sid.index[j]]]))
                # check if all entries have been checked
                if j + 1 == len(s_sorted):
                    done = True
            else: 
                # remember the indices from the second relation
                s_sorted = s_sorted[j:]
                sid = sid[j:]
                break
            j += 1
        # check if all entries have already been checked
        if done:
            break
            
    result = [item for sublist in result for item in sublist]
    return result, len(result)

# this should be the most efficient approach
def jvec_ineqjoin(R, S, r, s, op):
    # initialize the arrays in the right order
    r_sorted = np.sort(R[r])
    rid = np.argsort(R[r])
    s_sorted = np.sort(S[s])
    sid = np.argsort(S[s])
    if op in [operator.gt, operator.ge]:
        r_sorted = r_sorted[::-1]
        rid = rid[::-1]
        s_sorted = s_sorted[::-1]
        sid = sid[::-1]
    
    result = []
    done = False
    # check for the inequality constraints
    for i in range(len(r_sorted)):
        while 0 < len(s_sorted): 
            if op(r_sorted[i], s_sorted[0]):
                result.append(pairs([rid[rid.index[i]]], list(sid[0:])))
                break
            else: 
                # delete indices from list
                if len(s_sorted) > 1:
                    s_sorted = s_sorted[1:]
                    sid = sid[1:]
                else:
                    done = True
                    break
        # check if all entries have already been checked
        if done:
            break
            
    result = [item for sublist in result for item in sublist]
    return result, len(result)
        

# function to compute the intersection of a list of tuple pairs efficiently
def intersect_pairs(pair_lists, pair_list_lengths):
    # start with the shortes pair lists
    length_order = np.argsort(pair_list_lengths)
    # start the intersection
    result = pair_lists[length_order[0]]
    for i in range(1, len(length_order)):
        result = set(result).intersection(set(pair_lists[length_order[i]]))
    return result

# computes the antijoin with multiple join predicates
def naive_ineqjoin_multicond_OLD(R, S, r, s, op):
    # check if the arguments are consistent
    condition_len = len(op)
    assert len(s) == condition_len
    assert len(r) == condition_len
    # for each join condition check the valid tuples
    results = np.repeat(None, condition_len)
    res_lengths = np.repeat(0, condition_len)
    for i in range(condition_len):
        results[i], res_lengths[i] = naive_ineqjoin(R, S, r[i], s[i], op[i])
    for i in range(condition_len - 1):
        results[i + 1] = set(results[i]).intersection(set(results[i + 1]))
    return list(results[-1])
        
# computes the antijoin with multiple join predicates
def naive_ineqjoin_multicond(R, S, r, s, op):
    # check if the arguments are consistent
    condition_len = len(op)
    assert len(s) == condition_len
    assert len(r) == condition_len
    # for each join condition check the valid tuples
    results = np.repeat(None, condition_len)
    res_lengths = np.repeat(0, condition_len)
    for i in range(condition_len):
        results[i], res_lengths[i] = naive_ineqjoin(R, S, r[i], s[i], op[i])
    # only consider tuples which fulfill every join condition
    result = intersect_pairs(results, res_lengths)
    return result

# computes the antijoin with multiple join predicates (optimized for low selectivity)
def naive_ineqjoin_lowsel_multicond(R, S, r, s, op):
    # check if the arguments are consistent
    condition_len = len(op)
    assert len(s) == condition_len
    assert len(r) == condition_len
    # for each join condition check the valid tuples
    results = np.repeat(None, condition_len)
    res_lengths = np.repeat(0, condition_len)
    for i in range(condition_len):
        results[i], res_lengths[i] = naive_ineqjoin_lowsel(R, S, r[i], s[i], op[i])
    # only consider tuples which fulfill every join condition
    result = intersect_pairs(results, res_lengths)
    return result
   

# compute the antijoin with multiple join predicates by estimating selectivity
def flexible_ineqjoin_multicond(R, S, r, s, op, sample_p = 0.05):
    # check if the arguments are consistent
    condition_len = len(op)
    assert len(s) == condition_len
    assert len(r) == condition_len
    # for each join condidtion check the valid tuples
    results = np.repeat(None, condition_len)
    res_lengths = np.repeat(0, condition_len)
    for i in range(condition_len):
        n_R = int(np.ceil(len(R) * sample_p))
        n_S = int(np.ceil(len(S) * sample_p))
        R_samp = R.sample(n_R)
        S_samp = S.sample(n_S)
        _, sample_res_len = naive_ineqjoin(R_samp, S_samp, r[i], s[i], op[i])
        #estimate selectivity
        sel = sample_res_len / (n_R * n_S)
        # take optimal algorithm dependent on selectivity
        if sel < 0.5:
            results[i], res_lengths[i] = ivec_ineqjoin(R, S, r[i], s[i], op[i])
        else:
            results[i], res_lengths[i] = naive_ineqjoin(R, S, r[i], s[i], op[i])
    # only consider tuples which fulfill every join condition
    result = intersect_pairs(results, res_lengths)
    return result

# computes the inequality join hopefully very efficient
def ivec_ineqjoin_multicond(R, S, r, s, op):
    # check if the arguments are consistent
    condition_len = len(op)
    assert len(s) == condition_len
    assert len(r) == condition_len
    # for each join condition check the valid tuples
    results = np.repeat(None, condition_len)
    res_lengths = np.repeat(0, condition_len)
    for i in range(condition_len):
        results[i], res_lengths[i] = ivec_ineqjoin(R, S, r[i], s[i], op[i])
    # only consider tuples which fulfill every join condition
    result = intersect_pairs(results, res_lengths)
    return result

# computes the inequality join hopefully very efficient
def jvec_ineqjoin_multicond(R, S, r, s, op):
    # check if the arguments are consistent
    condition_len = len(op)
    assert len(s) == condition_len
    assert len(r) == condition_len
    # for each join condition check the valid tuples
    results = np.repeat(None, condition_len)
    res_lengths = np.repeat(0, condition_len)
    for i in range(condition_len):
        results[i], res_lengths[i] = jvec_ineqjoin(R, S, r[i], s[i], op[i])
    # only consider tuples which fulfill every join condition
    result = intersect_pairs(results, res_lengths)
    return result

# computes the permutation array for the IE Join
def compute_permutation_array(arr1, arr2):
    assert len(arr1) == len(arr2)
    perm_arr = np.repeat(0, len(arr1))
    for i in range(len(arr2)):
        perm_arr[i] = int(np.where(arr1 == arr2[i])[0])
    return perm_arr

# compute the offset from a tuple within the relation
def compute_offset(new_tuple, relation, by, ascending):
    union = relation.append(new_tuple)
    union.index = list(relation.index) + ["findme"]
    # order union
    union = union.sort_values(by = by, ascending = ascending)
    offset = int(np.where(union.index == "findme")[0])
    return offset

# computes the IE_join with two join predicates
def IE_join(R, S, r, s, op):
    # check if there are two join predicates
    assert len(op) == 2
    assert len(s) == 2
    assert len(r) == 2
    
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
        
    
    Afterwards compute offsets
    """
    
    # find out the necessary order
    if op[0] in [operator.gt, operator.ge] and op[1] in [operator.gt, operator.ge]:
        ascending0 = [False, False]
        ascending1 = [True, False]
    elif op[0] in [operator.lt, operator.le] and op[1] in [operator.gt, operator.ge]:
        ascending0 = [True, False]
        ascending1 = [True, True]
    elif op[0] in [operator.gt, operator.ge] and op[1] in [operator.lt, operator.le]:
        ascending0 = [False, True]
        ascending1 = [False, False]
    elif op[0] in [operator.lt, operator.le] and op[1] in [operator.lt, operator.le]:
        ascending0 = [True, True]
        ascending1 = [False, True]
    
    # apply the order to the relations accordingly
    R0 = R.sort_values(by = r, ascending = ascending0)
    S0 = S.sort_values(by = s, ascending = ascending0)
    R1 = R.sort_values(by = r[::-1], ascending = ascending1)
    S1 = S.sort_values(by = s[::-1], ascending = ascending1)
    # compute the permutation arrays
    p_r = compute_permutation_array(R0.index, R1.index)
    p_s = compute_permutation_array(S0.index, S1.index)
    # compute the offset arrays
    o0 = np.repeat(0, len(R0))
    o1 = np.repeat(0, len(R1))
    
    # this is potentially the bottleneck (how can this be implemented smarter?)
    for i in range(len(R0)):
        o0[i] = compute_offset(R0.loc[R0.index[i]], S0, s, ascending0)
        o1[i] = compute_offset(R1.loc[R1.index[i]], S1, s[::-1], ascending1)
         
    B = np.zeros(len(S0))
    result = []
    
    # start the join process
    for i in range(len(R0)):
        # save the tuple for later usage
        r1_i_id = R1.index[i]
        r1_i_tup = R1.loc[r1_i_id]
        # check if it's the first tuple
        if i == 0:
            start = 0
        else:
            start = o1[i - 1]
        # fill up binary index structure
        for j in range(start, o1[i]):
            B[p_s[j]] = 1
        # check for pairs fulfilling the condition
        off1 = o0[p_r[i]]
        for k in range(off1, len(S0)):
            if B[k] == 1:
                # check if constraint is fulfilled
                s0_k_id = S0.index[k]
                s0_k_tup = S0.loc[s0_k_id]
                if op[0](r1_i_tup[r[0]], s0_k_tup[s[0]]) and op[1](r1_i_tup[r[1]], s0_k_tup[s[1]]):
                    result.append((r1_i_id, s0_k_id))
    
    return result

def nested_loop_ineqjoin(R, S, r, s, op):
    # check if the arguments are consistent
    condition_len = len(op)
    assert len(s) == condition_len
    assert len(r) == condition_len
    result = []
    # loop over all tuples in R and S and check join condition
    for i in range(len(R)):
        R_i = R.loc[i]
        for j in range(len(S)):
            S_j = S.loc[j]
            pred_fulfilled = True
            for k in range(condition_len):
                if not op[k](R_i[k], S_j[k]):
                    pred_fulfilled = False
                    break
            if pred_fulfilled:
                result.append((i, j))
    return result