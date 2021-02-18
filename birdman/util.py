from typing import List

from cmdstanpy.stanfit import CmdStanMCMC
import numpy as np
import pandas as pd
import xarray as xr


def alr_to_clr(x: np.ndarray) -> np.ndarray:
    """Convert ALR coordinates to centered CLR coordinates.

    :param x: Matrix of ALR coordinates (features x draws)
    :type x: np.ndarray

    :returns: Matrix of centered CLR coordinates
    :rtype: np.ndarray
    """
    num_draws = x.shape[1]
    z = np.zeros((1, num_draws))
    x_clr = np.vstack((z, x))
    x_clr = x_clr - x_clr.mean(axis=0).reshape(1, -1)
    return x_clr


def convert_beta_coordinates(beta: np.ndarray) -> np.ndarray:
    """Convert feature-covariate coefficients from ALR to CLR.

    :param beta: Matrix of beta ALR coordinates (n draws x p covariates x
        d features)
    :type beta: np.ndarray

    :returns: Matrix of beta CLR coordinates (p covariates x (d+1) features x
        n draws)
    :rtype: np.ndarray
    """
    # axis moving is an artifact of previous PyStan implementation
    # want dims to be (p covariates x d features x n draws)
    # TODO: make this function work on the original dimensions
    beta = np.moveaxis(beta, [1, 2, 0], [0, 1, 2])
    num_covariates, num_features, num_draws = beta.shape
    beta_clr = np.zeros((num_covariates, num_features+1, num_draws))
    for i in range(num_covariates):  # TODO: vectorize
        beta_clr[i, :, :] = alr_to_clr(beta[i, :, :])
    return beta_clr
