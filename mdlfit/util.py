# encoding: utf-8
# pylint: disable=C0103
# pylint: disable=too-many-arguments
"""
Util
====

Miscellaneous utility functions
-------------------------------
.. autosummary::
    :toctree: generated/

    log2
    metric_levels
    find_nearest_values
    compute_description_length
    optimal_value
"""


import warnings
import numpy as np

__all__ = ['log2', 'metric_levels', 'optimal_value']


def log2(value):
    """ Function to compute log2 checking for nan values.
        A nan value is substituted by 0 and a warning is raised.

    Parameters
    ----------
    value : float
        input value

    Returns
    -------
    logval : float
        returned value

    """
    # compute log2 value
    logval = np.log2(value)

    # check if is nan
    if np.isinf(logval):
        logval = 0
        warnings.warn("Warning: nan value found, substitued by zero. ", RuntimeWarning)

    return logval


def metric_levels(signature, beat_subdivisions):
    """ Given a time signature and the number of subdivision per beat
        this function returns a list indicating the number of metric
        levels in which a subdivision position is present

    Parameters
    ----------
    signature : str
        string denoting the time signature to consider.
    beat_subdivisions : int
        number of (equal) subdivisions of each beat.

    Returns
    -------
    levels : list
        list of the number of metric levels in which each subdivision position is present

    """
    # time signature
    if signature == '4/4':
        # number of subdivision per beat
        if beat_subdivisions == 2:
            levels = [4, 1, 2, 1, 3, 1, 2, 1]

        elif beat_subdivisions == 4:
            levels = [5, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1]

        else:
            warnings.warn("Number of subdivision per beat not implemented yet. ", RuntimeWarning)
    elif signature == '2/4':
        if beat_subdivisions == 2:
            levels = [3, 1, 2, 1]

        elif beat_subdivisions == 4:
            levels = [4, 1, 2, 1, 3, 1, 2, 1]

        else:
            warnings.warn("Number of subdivision per beat not implemented yet. ", RuntimeWarning)

    else:
        warnings.warn("Time signature not implemented yet. ", RuntimeWarning)


    return levels

def find_nearest_values(array, value):
    """Find indexes of the two nearest values of an array to a given value

    Parameters
    ----------
    array (numpy.ndarray)  : array
    value (float)          : value

    Returns
    -------
    idx1 (int) : index of nearest value in the array
    idx2 (int) : index of second nearest value in the array
    """

    # index of nearest value in the array
    idx1 = (np.abs(array-value)).argmin()
    # check if value is bigger or smaller than nearest value
    if array[idx1] >= value:
        idx2 = idx1 - 1
    else:
        idx2 = idx1 + 1

    return idx1, idx2


def compute_description_length(val, n, n1):
    """Compute description length for a given parameter

    Parameters
    ----------
    val : float
        input value
    n : int
        total number of elements
    n1 : int
        total number of ones

    Returns
    -------
    dl_val (float) : description length value
    """

    if val in (0, 1):
        dl_val = np.inf
    else:
        dl_val = -(n1 * log2(val) + (n-n1) * log2(1-val))

    return dl_val


def optimal_value(d, val, n, n1):
    """Compute the optimal discrete value of the parameters given the precision

    Parameters
    ----------
    d : float
        precision value
    val : float
        input value
    n : int
        total number of elements
    n1 : int
        total number of ones

    Returns
    -------
    d_val : float
        returns discrete optimal value

    """

    if val in (0, 1):
        d_val = val
    else:
        # grid of parameter values
        grid = np.arange(0, 1, 1/d)
        # find the indexes of the nearest values in the grid
        idx1, idx2 = find_nearest_values(grid, val)
        # nearest values in the grid
        val1 = grid[idx1]
        val2 = grid[idx2]
        # description length values
        dl_val1 = compute_description_length(val1, n, n1)
        dl_val2 = compute_description_length(val2, n, n1)
        # check which parameter values gives a smaller description length
        if dl_val1 < dl_val2:
            d_val = val1
        else:
            d_val = val2

    return d_val
