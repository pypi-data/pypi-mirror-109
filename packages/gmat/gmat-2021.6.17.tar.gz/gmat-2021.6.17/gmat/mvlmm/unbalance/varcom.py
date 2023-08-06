import logging

from gmat.mvlmm.unbalance._pre_data import _pre_data
from gmat.mvlmm.unbalance._emai import _emai


def varcom(data_file, id, trait, agmat_file, fix=None, init=None, maxiter=100, cc_par=1.0e-8, cc_gra=1.0e-3,
                     em_weight_step=0.01, prefix_outfile='mvlmm_varcom'):
    """
    Estimate the variances for the multivariate linear mixed model.
    :param data_file:
    :param trait:
    :param agmat_file:
    :param fix:
    :param init:
    :param maxiter:
    :param cc_par:
    :param cc_gra:
    :param em_weight_step:
    :param prefix_outfile:
    :return:
    """
    logging.info("######################")
    logging.info("###Prepare the data###")
    logging.info("######################")
    y_lst, xmat_lst, zmat_lst, ag, error_lst, _ = _pre_data(data_file, id, trait, agmat_file, fix=fix)
    var_df = _emai(y_lst, xmat_lst, zmat_lst, ag, error_lst, init=init, maxiter=maxiter, cc_par=cc_par,
                      cc_gra=cc_gra, em_weight_step=em_weight_step, out_file=prefix_outfile)
    return var_df
