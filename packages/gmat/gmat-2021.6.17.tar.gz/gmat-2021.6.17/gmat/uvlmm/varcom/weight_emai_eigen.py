import logging
import numpy as np
import pandas as pd
from scipy import linalg
from pysnptools.snpreader import Bed
from tqdm import tqdm
from gmat.process_plink.process_plink import impute_geno
from scipy.stats import chi2
from scipy.sparse import csc_matrix
from patsy import dmatrix
from collections import OrderedDict
from functools import reduce
from scipy.stats import chi2


def weight_emai_eigen(pheno_file, agmat_file, class_lst=None, fix=None, maxiter0=100):
    """
    run GWAS based on linear mixed model and put one snp in each analysis.
    :param pheno_file: phenotypic file with head rows. The fist column is individual id. The last column is phenotypic values.
    Class variates and covariates are in the middle columns. Missing values in the phenotypic file can be
    expressed as 'NA', 'NaN', 'nan', 'na'.
    :param agmat_file: the prefix for the additive genomic relationship matrix file.
    :param class_lst: a list for class variates
    :param fix: formula for the fix effect. Eg. fix='sex + herd'
    :param maxiter0: the maximum number of iteration for variance estimation in the null model
    :return:
    """
    logging.info("###Prepare the phenotypic values, covariates and genomic matrix")
    y, xmat, zmat, ag, id_keep, xmat_ind = _pre_pheno(pheno_file, agmat_file, class_lst, fix)
    logging.info("###Estimate the variances in the null model.")
    init = np.array([np.var(y) / 2] * 2)
    gmat_eigenvals, gmat_eigenvecs = linalg.eigh(zmat.dot((zmat.dot(ag)).T))
    gmat_eigenvals = np.array(gmat_eigenvals).reshape(-1, 1)
    y_trans = np.dot(gmat_eigenvecs.T, y)  # transform the phenotypic values
    xmat_trans = np.dot(gmat_eigenvecs.T, xmat)  # transform the fixed effects
    var, convergence = _weight_emai_eigen(y_trans, xmat_trans, gmat_eigenvals, init=init, maxiter=maxiter0, cc=1.0e-8)
    logging.info('Whether converge?: {}'.format(convergence))
    logging.info('The estimated variances: {}'.format(var))
    logging.info("###Test the significance of fixed effects###")
    vmat = 1.0 / (gmat_eigenvals * var[0] + var[1])
    vx = np.multiply(vmat, xmat_trans)
    xvx = np.dot(xmat_trans.T, vx)
    xvx = linalg.inv(xvx)
    xvy = np.dot(vx.T, y_trans)
    eff = np.dot(xvx, xvy)
    for key, value in xmat_ind.items():
        logging.info("***{}: ".format(key))
        logging.info("Effect: {}".format(eff[value, -1]))
        logging.info("Covariance: {}".format(xvx[value, value]))
        p_val = chi2.sf(np.sum(reduce(np.dot, [eff[value, :].T, linalg.inv(xvx[value, :][:, value]), eff[value, :]])), len(value))
        logging.info("P value: {}".format(p_val))


def _pre_pheno(pheno_file, agmat_file, class_lst, fix):
    id_in_agmat = []
    with open(agmat_file + '.id') as fin:
        for line in fin:
            arr = line.split()
            id_in_agmat.append(arr[0])
    data_df = pd.read_csv(pheno_file, sep='\s+', header=0)
    data_df = data_df.dropna()
    col_names = data_df.columns
    class_lst2 = [col_names[0]]
    if class_lst is not None:
        class_lst2 = class_lst + class_lst2
    for val in col_names:
        if val in class_lst2:
            data_df[val] = data_df[val].astype('str')
        else:
            data_df[val] = data_df[val].astype('float')
    id_keep = []  # keep the id both in the agmat file and pheno file, without missing phenotypes and covariates.
    for i in range(data_df.shape[0]):
        if data_df.iloc[i, 0] in id_in_agmat:
            id_keep.append(True)
        else:
            id_keep.append(False)
    data_df = data_df.iloc[id_keep, :]
    id_keep = list(data_df.iloc[:, 0])
    y = np.array(data_df.iloc[:, -1]).reshape(-1, 1)
    xmat = np.ones((y.shape[0], 1))
    xmat_ind = OrderedDict()
    xmat_ind['Intercept'] = [0]
    if fix is not None:
        xmat = dmatrix(fix, data_df)
        xcol_names = xmat.design_info.column_names
        xmat = np.asarray(xmat)
        _, r = np.linalg.qr(xmat)
        indexes = np.absolute(np.diag(r)) >= 1e-10
        xcol_names = np.array(xcol_names)[indexes]
        for i in range(1, len(xcol_names)):
            key = xcol_names[i].split('[')[0]
            try:
                xmat_ind[key].append(i)
            except Exception as _:
                xmat_ind[key] = [i]
        xmat = xmat[:, indexes]
    val = 0
    id_dct = {}
    col = []
    for v in id_keep:
        if v not in id_dct:
            id_dct[v] = val
            val += 1
        col.append(id_dct[v])
    row = range(len(id_keep))
    zmat = csc_matrix(([1.0]*len(row), (row, col)))
    ag = np.zeros((len(id_dct), len(id_dct)))
    with open(agmat_file + '.agrm.id_fmt') as fin:
        for line in fin:
            arr = line.split()
            try:
                ag[id_dct[arr[0]], id_dct[arr[1]]] = ag[id_dct[arr[1]], id_dct[arr[0]]] = float(arr[2])
            except Exception as e:
                del e
    return y, xmat, zmat, ag, id_keep, xmat_ind


def _weight_emai_eigen(y_trans, xmat_trans, gmat_eigenvals, init=None, maxiter=100, cc=1.0e-8):
    fd_mat = np.zeros(2)
    ai_mat = np.zeros((2, 2))
    em_mat = np.zeros((2, 2))
    num_id = gmat_eigenvals.shape[0]
    cc_val = 1000.0
    var = np.array(init)
    var_update = var * 1000
    delta = var_update - var
    convergence = False
    for i in range(maxiter):
        logging.info("Iteration: {}".format(i+1))
        vmat = 1.0 / (gmat_eigenvals * var[0] + var[1])
        vx = np.multiply(vmat, xmat_trans)
        xvx = np.dot(xmat_trans.T, vx)
        xvx = linalg.inv(xvx)
        # py
        xvy = np.dot(vx.T, y_trans)
        y_xb = y_trans - np.dot(xmat_trans, np.dot(xvx, xvy))
        py = np.multiply(vmat, y_xb)
        # add_py p_add_py
        add_py = np.multiply(gmat_eigenvals, py)
        xvy = np.dot(vx.T, add_py)
        y_xb = add_py - np.dot(xmat_trans, np.dot(xvx, xvy))
        p_add_py = np.multiply(vmat, y_xb)
        # res_py p_res_py
        res_py = py.copy()
        xvy = np.dot(vx.T, res_py)
        y_xb = res_py - np.dot(xmat_trans, np.dot(xvx, xvy))
        p_res_py = np.multiply(vmat, y_xb)
        # fd
        tr_vd = np.sum(np.multiply(vmat, gmat_eigenvals))
        xvdvx = np.dot(xmat_trans.T, vmat * gmat_eigenvals * vx)
        tr_2d = np.sum(np.multiply(xvdvx, xvx))
        ypvpy = np.sum(np.dot(py.T, add_py))
        fd_mat[0] = 0.5 * (-tr_vd + tr_2d + ypvpy)
        tr_vd = np.sum(vmat)
        xvdvx = np.dot(xmat_trans.T, vmat * vx)
        tr_2d = np.sum(np.multiply(xvdvx, xvx))
        ypvpy = np.sum(np.dot(py.T, res_py))
        fd_mat[1] = 0.5 * (-tr_vd + tr_2d + ypvpy)
        # AI
        ai_mat[0, 0] = np.sum(np.dot(add_py.T, p_add_py))
        ai_mat[0, 1] = ai_mat[1, 0] = np.sum(np.dot(add_py.T, p_res_py))
        ai_mat[1, 1] = np.sum(np.dot(res_py.T, p_res_py))
        ai_mat = 0.5 * ai_mat
        # EM
        em_mat[0, 0] = num_id / (2 * var[0] * var[0])
        em_mat[1, 1] = num_id / (2 * var[1] * var[1])
        for j in range(0, 51):
            gamma = j * 0.02
            wemai_mat = (1 - gamma) * ai_mat + gamma * em_mat
            delta = np.dot(linalg.inv(wemai_mat), fd_mat)
            var_update = var + delta
            if min(var_update) > 0:
                logging.info('EM weight value: {}'.format(gamma))
                break
        # Convergence criteria
        logging.info('Updated variances: {}'.format(var_update))
        cc_val = np.sum(pow(delta, 2)) / np.sum(pow(var_update, 2))
        cc_val = np.sqrt(cc_val)
        var = var_update.copy()
        logging.info("CC: {}".format(cc_val))
        if cc_val < cc:
            break
    if cc_val < cc:
        convergence = True
    return var, convergence
