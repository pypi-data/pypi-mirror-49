#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 06:24:12 2018

@author: prmiles
"""
import numpy as np
from scipy import pi, sin, cos
import sys
import math


def check_settings(default_settings, user_settings=None):
    '''
    Check user settings with default.

    Recursively checks elements of user settings against the defaults
    and updates settings as it goes.  If a user setting does not exist
    in the default, then the user setting is added to the settings.
    If the setting is defined in both the user and default settings,
    then the user setting overrides the default.  Otherwise, the default
    settings persist.

    Args:
        * **default_settings** (:py:class:`dict`): Default settings for \
        particular method.

    Kwargs:
        * **user_settings** (:py:class:`dict`): User defined settings. \
          Default: `None`

    Returns:
        * (:py:class:`dict`): Updated settings.
    '''
    settings = default_settings.copy()  # initially define settings as default
    options = list(default_settings.keys())  # get default settings
    if user_settings is None:  # convert to empty dict
        user_settings = {}
    user_options = list(user_settings.keys())  # get user settings
    for uo in user_options:  # iterate through settings
        if uo in options:
            # check if checking a dictionary
            if isinstance(settings[uo], dict):
                settings[uo] = check_settings(settings[uo], user_settings[uo])
            else:
                settings[uo] = user_settings[uo]
        if uo not in options:
            settings[uo] = user_settings[uo]
    return settings


def generate_subplot_grid(nparam=2):
    '''
    Generate subplot grid.

    For example, if `nparam` = 2, then the subplot will have
    2 rows and 1 column.

    Kwargs:
        * **nparam** (:py:class:`int`): Number of parameters. \
          Default: `2`

    Returns:
        * **ns1** (:py:class:`int`): Number of rows in subplot
        * **ns2** (:py:class:`int`): Number of columns in subplot
    '''
    ns1 = math.ceil(math.sqrt(nparam))
    ns2 = round(math.sqrt(nparam))
    return ns1, ns2


def generate_names(nparam, names):
    '''
    Generate parameter name set.

    For example, if `nparam` = 4, then the generated names are::

        names = ['p_{0}', 'p_{1}', 'p_{2}', 'p_{3}']

    Args:
        * **nparam** (:py:class:`int`): Number of parameter names to generate
        * **names** (:py:class:`list`): Names of parameters provided by user

    Returns:
        * **names** (:py:class:`list`): List of strings - parameter names
    '''
    # Check if names defined
    if names is None:
        names = generate_default_names(nparam)
    # Check if enough names defined
    if len(names) != nparam:
        names = extend_names_to_match_nparam(names, nparam)
    return names


def generate_default_names(nparam):
    '''
    Generate generic parameter name set.

    For example, if `nparam` = 4, then the generated names are::

        names = ['$p_{0}$', '$p_{1}$', '$p_{2}$', '$p_{3}$']

    Args:
        * **nparam** (:py:class:`int`): Number of parameter names to generate

    Returns:
        * **names** (:py:class:`list`): List of strings - parameter names
    '''
    names = []
    for ii in range(nparam):
        names.append(str('$p_{{{}}}$'.format(ii)))
    return names


def extend_names_to_match_nparam(names, nparam):
    '''
    Append names to list using default convention
    until length of names matches number of parameters.

    For example, if `names = ['name_1', 'name_2']` and `nparam = 4`, then
    two additional names will be appended to the `names` list.
    E.g.,::

        names = ['name_1', 'name_2', '$p_{2}$', '$p_{3}$']

    Args:
        * **names** (:py:class:`list`): Names of parameters provided by user
        * **nparam** (:py:class:`int`): Number of parameter names to generate

    Returns:
        * **names** (:py:class:`list`): List of strings - extended \
        list of parameter names
    '''
    if names is None:
        names = []
    n0 = len(names)
    for ii in range(n0, nparam):
        names.append(str('$p_{{{}}}$'.format(ii)))
    return names


# --------------------------------------------
def make_x_grid(x, npts=100):
    '''
    Generate x grid based on extrema.

    1. If `len(x) > 200`, then generates grid based on difference
    between the max and min values in the array.

    2. Otherwise, the grid is defined with respect to the array
    mean plus or minus four standard deviations.

    Args:
        * **x** (:class:`~numpy.ndarray`): Array of points

    Kwargs:
        * **npts** (:py:class:`int`): Number of points to use in \
          generated grid. Default: `100`

    Returns:
        * (:class:`~numpy.ndarray`): Uniformly spaced array of points \
        with shape :code:`(npts,1)`.
    '''
    xmin = min(x)
    xmax = max(x)
    xxrange = xmax-xmin
    if len(x) > 200:
        x_grid = np.linspace(xmin-0.08*xxrange, xmax+0.08*xxrange, npts)
    else:
        x_grid = np.linspace(np.mean(x)-4*np.std(x, ddof=1),
                             np.mean(x)+4*np.std(x, ddof=1), npts)
    return x_grid.reshape(x_grid.shape[0], 1)  # returns 1d column vector


# --------------------------------------------
# see MASS 2nd ed page 181.
def iqrange(x):
    '''
    Interquantile range of each column of x.

    Args:
        * **x** (:class:`~numpy.ndarray`): Array of points.

    Returns:
        * (:class:`~numpy.ndarray`): Interquantile range - single \
        element array, `q3 - q1`.
    '''
    nr, nc = x.shape
    if nr == 1:  # make sure it is a column vector
        x = x.reshape(nc, nr)
        nr = nc
        nc = 1
    # sort
    x.sort()
    i1 = math.floor((nr + 1)/4)
    i3 = math.floor(3/4*(nr+1))
    f1 = (nr+1)/4-i1
    f3 = 3/4*(nr+1)-i3
    q1 = (1-f1)*x[int(i1), :] + f1*x[int(i1)+1, :]
    q3 = (1-f3)*x[int(i3), :] + f3*x[int(i3)+1, :]
    return q3-q1


def gaussian_density_function(x, mu=0, sigma2=1):
    '''
    Standard normal/Gaussian density function.

    Args:
        * **x** (:py:class:`float`): Value of which to calculate probability.

    Kwargs:
        * **mu** (:py:class:`float`): Mean of Gaussian distribution. \
          Default: `0`
        * **sigma2** (:py:class:`float`): Variance of Gaussian \
          distribution. Default: `1`

    Returns:
        * **y** (:py:class:`float`): Likelihood of `x`.
    '''
    y = 1/math.sqrt(2*math.pi*sigma2)*math.exp(-0.5*(x-mu)**2/sigma2)
    return y


def scale_bandwidth(x):
    '''
    Scale bandwidth of array.

    Args:
        * **x** (:class:`~numpy.ndarray`): Array of points - column of chain.

    Returns:
        * **s** (:class:`~numpy.ndarray`): Scaled bandwidth - single \
        element array.
    '''
    n = len(x)
    if iqrange(x) <= 0:
        s = 1.06*np.array([np.std(x, ddof=1)*n**(-1/5)])
    else:
        s = 1.06*np.array([min(np.std(x, ddof=1), iqrange(x)/1.34)*n**(-1/5)])
    return s


# --------------------------------------------
def generate_ellipse(mu, cmat, ndp=100):
    '''
    Generates points for a probability contour ellipse

    Args:
        * **mu** (:class:`~numpy.ndarray`): Mean values
        * **cmat** (:class:`~numpy.ndarray`): Covariance matrix

    Kwargs:
        * **npd** (:py:class:`int`): Number of points to generate. \
          Default: `100`

    Returns:
        * **x** (:class:`~numpy.ndarray`): x-points
        * **y** (:class:`~numpy.ndarray`): y-points
    '''
    # check shape of covariance matrix
    if cmat.shape != (2, 2):
        sys.exit('covariance matrix must be 2x2')
    if check_symmetric(cmat) is not True:
        sys.exit('covariance matrix must be symmetric')
    # define t space
    t = np.linspace(0, 2*pi, ndp)
    pdflag, R = is_semi_pos_def_chol(cmat)
    if pdflag is False:
        sys.exit('covariance matrix must be positive definite')
    x = mu[0] + R[0, 0]*cos(t)
    y = mu[1] + R[0, 1]*cos(t) + R[1, 1]*sin(t)
    return x, y


def generate_ellipse_plot_points(x, y, ndp=100):
    '''
    Generates points for a probability contour ellipse for 2 columns of chain

    Args:
        * **x** (:class:`~numpy.ndarray`): chain 1
        * **y** (:class:`~numpy.ndarray`): chain 2

    Kwargs:
        * **npd** (:py:class:`int`): Number of points to generate. \
          Default: `100`

    Returns:
        * (:py:class:`dict`): 50% and 95% probability contours.
    '''
    c50 = 1.3863  # critical values from chisq(2) distribution
    c95 = 5.9915
    sig = np.cov(x.reshape(x.size,), y.reshape(y.size,))
    mu = np.mean(np.array([x, y]), axis=1)
    xe50, ye50 = generate_ellipse(mu, c50*sig, ndp=ndp)
    xe95, ye95 = generate_ellipse(mu, c95*sig, ndp=ndp)
    return {'xe50': xe50, 'ye50': ye50, 'xe95': xe95, 'ye95': ye95}


def check_symmetric(a, tol=1e-8):
    '''
    Check if array is symmetric by comparing with transpose.

    Args:
        * **a** (:class:`~numpy.ndarray`): Array to test.

    Kwargs:
        * **tol** (:py:class:`float`): Tolerance for testing equality. \
          Default: `1e-8`

    Returns:
        * (:py:class:`bool`): True -> symmetric, False -> not symmetric.
    '''
    return np.allclose(a, a.T, atol=tol)


def is_semi_pos_def_chol(x):
    '''
    Check if matrix is semi positive definite by calculating Cholesky
    decomposition.

    Args:
        * **x** (:class:`~numpy.ndarray`): Matrix to check

    Returns:
        * If matrix is `not` semi positive definite return :code:`False, None`
        * If matrix is semi positive definite return :code:`True` and the \
        Upper triangular form of the Cholesky decomposition matrix.
    '''
    c = None
    try:
        c = np.linalg.cholesky(x)
        return True, c.transpose()
    except np.linalg.linalg.LinAlgError:
        return False, c


def append_to_nrow_ncol_based_on_shape(sh, nrow, ncol):
    '''
    Append to list based on shape of array

    Args:
        * **sh** (:py:class:`tuple`): Shape of array.
        * **nrow** (:py:class:`list`): List of number of rows
        * **ncol** (:py:class:`list`): List of number of columns

    Returns:
        * **nrow** (:py:class:`list`): List of number of rows
        * **ncol** (:py:class:`list`): List of number of columns
    '''
    if len(sh) == 1:
        nrow.append(sh[0])
        ncol.append(1)
    else:
        nrow.append(sh[0])
        ncol.append(sh[1])
    return nrow, ncol


def setup_subsample(skip, maxpoints, nsimu):
    '''
    Setup subsampling from posterior.

    When plotting the sampling chain, it is often beneficial to subsample
    in order to avoid to dense of plots.  This routine determines the
    appropriate step size based on the size of the chain (nsimu) and maximum
    points allowed to plot (maxpoints).  The function checks if the
    size of the chain exceeds the maximum number of points allowed in the
    plot.  If yes, skip is defined such that every the max number of points
    are used and sampled evenly from the start to end of the chain.  Otherwise
    the value of skip is return as defined by the user.  A subsample index
    is then generated based on the value of skip and the number of simulations.

    Args:
        * **skip** (:py:class:`int`): User defined skip value.
        * **maxpoints** (:py:class:`int`): Maximum points allowed in each plot.

    Returns:
        * (:py:class:`int`): Skip value.
    '''
    if nsimu > maxpoints:
        skip = int(np.floor(nsimu/maxpoints))
    return np.arange(0, nsimu, skip)
