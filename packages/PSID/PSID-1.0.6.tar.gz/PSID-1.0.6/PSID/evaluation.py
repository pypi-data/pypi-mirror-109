""" 
Copyright (c) 2020 University of Southern California
See full notice in LICENSE.md
Omid G. Sani and Maryam M. Shanechi
Shanechi Lab, University of Southern California

Tools for evaluating system identification
"""

import warnings

import numpy as np

from sklearn.metrics import r2_score


def evalPrediction(trueValue, prediction, measure):

    if measure == 'CC':
        n = trueValue.shape[1]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            R = np.corrcoef(trueValue, prediction, rowvar=False)
        perf = np.diag(R[n:, :n])
    elif measure == 'R2':
        perf = r2_score(trueValue, prediction, multioutput='raw_values')
    return perf
