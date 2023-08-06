import math
import numpy as np
from scipy import linalg
import datetime
import pandas as pd
import logging

from .common import *
from .pre_mat import *
from .iter_mat import *


def _emai(y, xmat, leg_tp, kin_eigen_val, init=None, maxiter=30, cc_par=1.0e-8, cc_gra=1.0e-6, em_weight_step=0.02, out_file="balance_varcom"):
    num_record = y.shape[0]*y.shape[1]*y.shape[2]
    ran_df = len(kin_eigen_val)
    cov_dim = leg_tp.shape[1]
    var_com = np.array(init)
    var_com_update = np.array(var_com)
    logging.info("initial variances: {}".format(var_com, dtype=str))
    cov = pre_cov_mat_eigen(cov_dim, var_com)
    if cov is None:
        logging.info('The covariances are not positive defined!')
        exit()
    cov_add, cov_per, cov_res = cov[:]
    var_ind_add = np.tril_indices_from(cov_add)
    var_ind_add = np.concatenate([np.zeros((len(var_ind_add[0]), 1)), np.array(var_ind_add).T], axis=1)
    var_ind_per = np.tril_indices_from(cov_per)
    var_ind_per = np.concatenate([np.ones((len(var_ind_per[0]), 1)), np.array(var_ind_per).T], axis=1)
    var_ind_res = np.array([[2, 1, 1]])
    var_ind = np.concatenate([var_ind_add, var_ind_per, var_ind_res], axis=0)
    var_ind = np.array(var_ind, dtype=np.int)
    kin_dct = {
        0: kin_eigen_val.reshape(len(kin_eigen_val), 1, 1),
        1: 1.0,
        2: 1.0
    }
    iter_count = 0
    delta = 1000.0
    cc_par_val = 1000.0
    cc_gra_val = 1000.0
    while iter_count < maxiter:
        iter_count += 1
        logging.info('***Start the iteration: {} ***'.format(iter_count))
        logging.info("fd and ai matrix")
        fd_mat, ai_mat = pre_fdai_mat_eigen_glm(y, xmat, leg_tp, kin_eigen_val, cov_add, cov_per, cov_res, var_com,
                                            var_ind, kin_dct)
        np.savetxt(out_file + '.fd', fd_mat)
        np.savetxt(out_file + '.ai', ai_mat)
        logging.info("EM matrix")
        em_mat = pre_em_mat_eigen(cov_dim, cov_add, cov_per, ran_df, var_com, num_record)
        np.savetxt(out_file + '.em', em_mat)
        gamma = -em_weight_step
        while gamma < 1.0:
            gamma = gamma + em_weight_step
            if gamma >= 1.0:
                gamma = 1.0
            wemai_mat = (1 - gamma) * ai_mat + gamma * em_mat
            delta = np.dot(linalg.inv(wemai_mat), fd_mat)
            var_com_update = var_com + delta
            cov = pre_cov_mat_eigen(cov_dim, var_com_update)
            if cov is not None:
                logging.info('EM weight value: ' + str(gamma))
                break
        logging.info('Updated variances: ' + ' '.join(np.array(var_com_update, dtype=str)))
        cov_add, cov_per, cov_res = cov[:]
        # Convergence criteria
        cc_par_val = np.sum(pow(delta, 2)) / np.sum(pow(var_com_update, 2))
        cc_par_val = np.sqrt(cc_par_val)
        cc_gra_val = np.sqrt(np.sum(pow(fd_mat, 2))) / len(var_com)
        var_com = var_com_update.copy()
        logging.info("Change in parameters, Norm of gradient vector: {} {}".format(cc_par_val, cc_gra_val))
        if cc_par_val < cc_par and cc_gra_val < cc_gra:
            break
    if cc_par_val < cc_par and cc_gra_val < cc_gra:
        logging.info("Variances Converged")
    else:
        logging.info("Variances Not Converged")
    var_pd = {'var': np.array(var_ind[:, 0]) + 1,
              "vari": np.array(var_ind[:, 1]) + 1,
              "varj": np.array(var_ind[:, 2]) + 1,
              "var_com": var_com}
    var_pd = pd.DataFrame(var_pd, columns=['var', "vari", "varj", "var_com"])
    return var_pd
