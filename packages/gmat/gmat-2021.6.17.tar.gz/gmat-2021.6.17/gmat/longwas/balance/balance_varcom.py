import os
import logging
from scipy import linalg
from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd
import gc


from ._pre_data import _pre_data
from ._common import _design_matrix, _leg_mt, _full_col_rank
from ._emai import _emai

def balance_varcom(data_file, id, tpoint, trait, gmat_file, tfix=None, fix=None, forder=3, rorder=3, na_method='omit',
                   init=None, maxiter=100, cc_par=1.0e-8, cc_gra=1.0e6, em_weight_step=0.001,
                   prefix_outfile='balance_varcom'):
    """
    Estimate variance parameters for balanced longitudinal data.
    :param data_file: the data file. The first row is the variate names whose first initial position is alphabetical.
    For the class variates, the first letter must be capital; for the covariates (continuous variates), the first letter
    must be lowercase.
    :param id: A class variate name which indicates the individual id column in the data file.
    :param tpoint: A list of corresponding time points for phenotypic values.
    :param trait: A list indicating the columns for recorded phenotypic values. The column index starts from 0 in the
    data file.
    :param gmat_file: the file for genomic relationship matrix. This file can be produced by
    gmat.gmatrix.agmat function using agmat(bed_file, inv=True, small_val=0.001, out_fmt='id_id_val')
    :param tfix: A class variate name for the time varied fixed effect. Default value is None. The value must be None
    in the current version.
    :param fix: Expression for the time independent fixed effect. Default value is None. The value must be None
    in the current version.
    :param forder: the order of Legendre polynomials for the time varied fixed effect. The default value is 3.
    :param rorder: the order of Legendre polynomials for time varied random effects (additive genetic effects and
    permanent environment effects). The default value is 3.
    :param na_method: The method to deal with missing values. The default value is 'omit'. 'omit' method will delete the
    row with missing values. 'include' method will fill the missing values with the adjacent values.
    :param init: the initial values for the variance parameters. The default value is None.
    :param maxiter: the maximum number of iteration. Default is 100.
    :param cc_par: Convergence criteria for the changed variance parameters. Default is 1.0e-8.
    :param cc_gra: Convergence criteria for the norm of gradient vector. Default is 1.0e6.
    :param em_weight_step: the step of the em weight. Default is 0.001.
    :param prefix_outfile: the prefix for the output file. Default is 'balance_varcom'.
    :return: the estimated variance parameters.
    """
    logging.info('################################################')
    logging.info('###Prepare the data for variances estimation.###')
    logging.info('################################################')
    y, xmat, leg_tp, var_com, ag_eigen_val = _pre_data(data_file, id, tpoint, trait, gmat_file, tfix=tfix, fix=fix,
                                forder=forder, rorder=rorder, na_method=na_method, init=init)
    logging.info('###################################################################')
    logging.info('###Start variances estimation for the balanced longitudinal data###')
    logging.info('###################################################################')
    res = _emai(y, xmat, leg_tp, ag_eigen_val, init=var_com, maxiter=maxiter, cc_par=cc_par,
                       cc_gra=cc_gra, em_weight_step=em_weight_step, out_file=prefix_outfile)
    var_file = prefix_outfile + '.var'
    res.to_csv(var_file, sep=' ', index=False)
    return res
