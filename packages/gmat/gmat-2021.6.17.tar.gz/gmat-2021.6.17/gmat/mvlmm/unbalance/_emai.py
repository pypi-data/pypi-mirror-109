import sys
import math
import numpy as np
import pandas as pd
from scipy import linalg
from scipy import sparse
from scipy.sparse import csr_matrix, block_diag, bmat
import logging
from functools import reduce


def _emai(y_lst, xmat_lst, zmat_lst, ag, error_lst, init=None, maxiter=200, cc_par=1.0e-8,
                      cc_gra=1.0e-3, em_weight_step=0.01, out_file='var_com'):
    def init_var(y_lst):
        """
        initialize the variances
        """
        y_var_lst = np.array(list(map(np.var, y_lst)))/2
        add_cov = np.diag(y_var_lst)
        add_ind = np.tril_indices_from(add_cov)
        error_cov = np.diag(y_var_lst)
        error_ind = np.tril_indices_from(error_cov)
        cov_ind = [1] * len(add_ind[0]) + [2] * len(error_ind[0])
        cov_ind_i = list(add_ind[0] + 1) + list(error_ind[0] + 1)
        cov_ind_j = list(add_ind[1] + 1) + list(error_ind[1] + 1)
        var_com = list(add_cov[add_ind]) + list(error_cov[error_ind])
        var_df = {'var': cov_ind,
                  "vari": cov_ind_i,
                  "varj": cov_ind_j,
                  "var_com": var_com}
        var_df = pd.DataFrame(var_df, columns=['var', "vari", "varj", "var_com"])
        return np.array(var_com), var_df
    var_com, var_df = init_var(y_lst)
    if init is not None:
        if len(var_com) != len(init):
            logging.error('The length of initial variances should be {}'.format(len(var_com)))
            sys.exit()
        else:
            var_com = np.array(init)
            var_df['var_com'] = var_com

    def pre_cov(y_lst, var_df):
        """
        return the covariance matrix. If one covariance matrix is not positive, return None.
        """
        add_cov = np.zeros((len(y_lst), len(y_lst)))
        add_cov[np.tril_indices(len(y_lst))] = np.array(var_df[var_df['var']==1].iloc[:, -1])
        add_cov = np.add(add_cov, np.tril(add_cov, -1).T)
        error_cov = np.zeros((len(y_lst), len(y_lst)))
        error_cov[np.tril_indices(len(y_lst))] = np.array(var_df[var_df['var'] == 2].iloc[:, -1])
        error_cov = np.add(error_cov, np.tril(error_cov, -1).T)
        try:
            linalg.cholesky(add_cov)
            linalg.cholesky(error_cov)
        except Exception as _:
                return None
        return add_cov, error_cov

    cov_lst = pre_cov(y_lst, var_df)
    if cov_lst is None:
        logging.error("ERROR: Initial variances is not positive define, please check!")
        sys.exit()
    add_cov, error_cov = cov_lst
    xmat_con = np.array(xmat_lst[0])
    for i in range(1, len(xmat_lst)):
        xmat_con = linalg.block_diag(xmat_con, xmat_lst[i])
    zmat_con = block_diag(zmat_lst, format='csr')
    y_con = np.concatenate(y_lst, axis=0)
    iter_count = 0
    cc_par_val = 1000.0
    cc_gra_val = 1000.0
    delta = 1000.0
    var_com_update = var_com * 1000
    logging.info("initial variances: {}".format(var_df))
    while iter_count < maxiter:
        iter_count += 1
        logging.info('***Start the iteration: {} ***'.format(iter_count))
        logging.info("Calculate V and P matrix")
        vmat = []
        for i in range(len(error_lst)):
            vec = []
            for j in range(len(error_lst[i])):
                vec.append(error_lst[i][j]*error_cov[i, j])
            vmat.append(vec)
        vmat = bmat(vmat, format='csr')
        vmat += zmat_con.dot((zmat_con.dot(linalg.kron(add_cov, ag))).T)
        vmat = linalg.inv(vmat)
        vxmat = np.dot(vmat, xmat_con)
        xvxmat = np.dot(xmat_con.T, vxmat)
        xvxmat = linalg.inv(xvxmat)
        pmat = vmat - reduce(np.dot, [vxmat, xvxmat, vxmat.T])
        pymat = np.dot(pmat, y_con)
        fd_mat = []
        wv_mat = []
        for i in range(add_cov.shape[0]):
            for j in range(i+1):
                add_cov_zeros = np.zeros((add_cov.shape[0], add_cov.shape[1]))
                add_cov_zeros[i, j] = add_cov_zeros[j, i] = 1.0
                temp = zmat_con.dot((zmat_con.dot(linalg.kron(add_cov_zeros, ag))).T)
                wv_mat.append(np.dot(temp, pymat))
                fd_val = -np.sum(pmat * temp) + np.sum(np.dot(pymat.T, wv_mat[-1]))
                fd_mat.append(fd_val*0.5)
        for i in range(error_cov.shape[0]):
            for j in range(i+1):
                error_cov_zeros = np.zeros((error_cov.shape[0], error_cov.shape[1]))
                error_cov_zeros[i, j] = error_cov_zeros[j, i] = 1.0
                error_mat = []
                for m in range(len(error_lst)):
                    vec = []
                    for n in range(len(error_lst[m])):
                        vec.append(error_lst[m][n] * error_cov_zeros[m, n])
                    error_mat.append(vec)
                error_mat = bmat(error_mat, format='csr')
                wv_mat.append(error_mat.dot(pymat))
                fd_val = -np.sum(pmat * error_mat.toarray()) + np.sum(np.dot(pymat.T, wv_mat[-1]))
                fd_mat.append(fd_val * 0.5)
        fd_mat = np.array(fd_mat)
        np.savetxt(out_file + '.fd', fd_mat)
        wv_mat = np.concatenate(wv_mat, axis=1)
        ai_mat = reduce(np.dot, [wv_mat.T, pmat, wv_mat])
        np.savetxt(out_file + '.ai', ai_mat)
        ind = np.tril_indices_from(add_cov)
        len_add_cov = len(ind[0])
        em_mat_add = np.zeros((len_add_cov, len_add_cov))
        for i in range(len_add_cov):
            for j in range(i+1):
                em_mat_add[i, j] = (add_cov[ind[0][i], ind[0][j]] * add_cov[ind[1][i], ind[1][j]] +
                                  add_cov[ind[0][i], ind[1][j]] * add_cov[ind[1][i], ind[0][j]]) / (2.0 * ag.shape[0])
        ind = np.tril_indices_from(error_cov)
        len_error_cov = len(ind[0])
        em_mat_error = np.zeros((len_error_cov, len_error_cov))
        for i in range(len_error_cov):
            for j in range(i + 1):
                em_mat_error[i, j] = (error_cov[ind[0][i], ind[0][j]] * error_cov[ind[1][i], ind[1][j]] +
                                    error_cov[ind[0][i], ind[1][j]] * error_cov[ind[1][i], ind[0][j]]) \
                        / (len(error_lst[ind[0][i]][ind[0][j]].data) + len(error_lst[ind[1][i]][ind[1][j]].data))
        em_mat = linalg.block_diag(em_mat_add, em_mat_error)
        em_mat = 2.0 * em_mat
        em_mat += np.tril(em_mat, k=-1).T
        em_mat = linalg.inv(em_mat)
        np.savetxt(out_file + '.em', em_mat)
        # Increase em weight to guarantee variances positive
        gamma = -em_weight_step
        while gamma < 1.0:
            gamma = gamma + em_weight_step
            if gamma >= 1.0:
                gamma = 1.0
            wemai_mat = (1 - gamma) * ai_mat + gamma * em_mat
            delta = np.dot(linalg.inv(wemai_mat), fd_mat)
            var_com_update = var_com + delta
            var_df['var_com'] = var_com_update
            cov_lst = pre_cov(y_lst, var_df)
            if cov_lst is not None:
                logging.info('EM weight value: ' + str(gamma))
                break
        var_df.to_csv(out_file + '.var', sep='\t', index=False)
        if cov_lst is None:
            logging.error("ERROR: Updated variances is not positive define!")
            sys.exit()
        add_cov, error_cov = cov_lst
        # Convergence criteria
        cc_par_val = np.sum(pow(delta, 2)) / np.sum(pow(var_com_update, 2))
        cc_par_val = np.sqrt(cc_par_val)
        cc_gra_val = np.sqrt(np.sum(pow(fd_mat, 2))) / len(var_com)
        var_com = var_com_update.copy()
        logging.info("Change in parameters: {}, Norm of gradient vector: {}".format(cc_par_val, cc_gra_val))
        if cc_par_val < cc_par and cc_gra_val < cc_gra:
            break
    if cc_par_val < cc_par and cc_gra_val < cc_gra:
        logging.info("Variances Converged")
    else:
        logging.info("Variances not Converged")
    var_df['var_com'] = var_com
    return var_df
