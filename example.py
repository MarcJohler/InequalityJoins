# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 00:52:08 2022

@author: Marc Johler
"""

import pandas as pd
import numpy as np
import operator
from classes import naive_antijoin, naive_antijoin_multicond

np.random.seed(42)
n1 = 20
duration1 = np.random.randint(100, size = n1)
cost1 = np.random.randint(100, size = n1)
R = {'duration':duration1, 'cost':cost1}
R = pd.DataFrame(R)

n2 = 20
duration2 = np.random.randint(100, size = n2)
cost2 = np.random.randint(100, size = n2)
S = {'duration':duration2, 'cost':cost2}
S = pd.DataFrame(S)

ajoin_result = naive_antijoin_multicond(R, S, ["duration", "cost"], ["duration", "cost"], [operator.lt, operator.gt])