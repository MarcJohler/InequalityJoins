# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 00:52:08 2022

@author: Marc Johler
"""

import pandas as pd
import numpy as np
import operator
from classes import naive_ineqjoin_multicond, IE_join

duration1 = np.array([140, 100, 90])
cost1 = np.array([10, 12, 5])
R = {'duration':duration1, 'cost':cost1}
R = pd.DataFrame(R)

duration2 = np.array([100, 120, 90, 90])
cost2 = np.array([6, 11, 10, 6])
S = {'duration':duration2, 'cost':cost2}
S = pd.DataFrame(S)

naive_join_result = naive_ineqjoin_multicond(R, S, ["duration", "cost"], ["duration", "cost"], [operator.le, operator.ge])
ie_join_result = IE_join(R, S, ["duration", "cost"], ["duration", "cost"], [operator.le, operator.ge])