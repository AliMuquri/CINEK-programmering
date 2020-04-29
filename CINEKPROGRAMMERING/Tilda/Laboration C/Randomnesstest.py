#Source copied from  https://gist.githubusercontent.com/Akaame/16e413c01f787ad85b3b7d0c91fe895d/raw/d71fca04bc89e4d44c7400344a66f5cbcc58c1f6/runs_test.py
# H0:  the sequence was produced in a random manner
# Ha:  the sequence was not produced in a random manner

# Read test data

import numpy as np
import scipy.stats as st

# Assuming number of runs greater than 10
def runs_test(d, v, alpha = 0.05):
    # Get positive and negative values
    mask = d > v
    # get runs mask
    p = mask == True
    n = mask == False
    xor = np.logical_xor(p[:-1], p[1:])
    # A run can be identified by positive
    # to negative (or vice versa) changes
    d = sum(xor) + 1 # Get number of runs
    n_p = sum(p) # Number of positives

    n_n = sum(n)

    # Temporary intermediate values
    tmp = 2 * n_p * n_n
    tmps = n_p + n_n

    # Expected value
    r_hat = np.float64(tmp) / tmps + 1
    # Variance
    s_r_squared=(r_hat-1)*(r_hat-2)/(tmps-1)
    #s_r_squared = (tmp*(tmp - tmps)) / (tmps*tmps*(tmps-1))

    # Standard deviation
    s_r =  np.sqrt(s_r_squared)
    # Test score
    z = (d - r_hat) / s_r

    # Get normal table
    z_alpha = st.norm.ppf(1-alpha)
    # Check hypothesis
    return z, z_alpha

# Load array
