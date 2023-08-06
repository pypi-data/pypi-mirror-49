# (c) 2012-2018 Dativa, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

#!python
#cython: language_level=3, boundscheck=False, wraparound=False, optimize.use_switch=True
cimport numpy as np
import numpy as np
import math
from itertools import combinations

cpdef inline float _get_marginal_score(int pop_size,
                                       list  pop_values,
                                       int item_label,
                                       np.ndarray[double, ndim=1]  scores,
                                       bint infer_missing):
    cdef double score = 0
    cdef double permutation_score
    cdef int i
    cdef int subset_label
    cdef double subset_score
    cdef double superset_score

    for i in range(0, pop_size):
        permutation_score = 0
        for c in combinations([p for p in pop_values if p != item_label], i):
            subset_label = sum(c)
            superset_score = scores[subset_label + item_label]
            subset_score = scores[subset_label]

            if subset_label > 0 and infer_missing and (superset_score == 0 or subset_score == 0):
                pass
            else:
                permutation_score = permutation_score + superset_score - subset_score

        score = score + permutation_score * math.factorial(i) * math.factorial(pop_size - i - 1)

    return score
