import os
import logging
from scipy import linalg
from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd
import gc

from ._common import _design_matrix, _leg_mt, _full_col_rank


def _pre_data(data_file, id, tpoint, trait, gmat_file, tfix=None, fix=None, forder=3, rorder=3, na_method='omit',
                   init=None):
    logging.info('***Read the data file***')
    logging.info('Data file: {}'.format(data_file))
    data_df = pd.read_csv(data_file, sep='\s+', header=0)
    logging.info('NA method: ' + na_method)
    if na_method == 'omit':
        data_df = data_df.dropna()
    elif na_method == 'include':
        data_df = data_df.fillna(method='ffill')
        data_df = data_df.fillna(method='bfill')
    else:
        logging.info('na_method does not exist: {}'.format(na_method))
        exit()
    col_names = data_df.columns
    logging.info('The column names of data file: {}'.format(list(col_names)))
    logging.info('Note: Variates beginning with a capital letter is converted into factors.')
    class_vec = []
    for val in col_names:
        if not val[0].isalpha():
            logging.info("The first character of columns names must be alphabet!")
            exit()
        if val[0] == val.capitalize()[0]:
            class_vec.append(val)
            data_df[val] = data_df[val].astype('str')
        else:
            try:
                data_df[val] = data_df[val].astype('float')
            except Exception as e:
                logging.info(e)
                logging.info(val + " column may contain string, please check!")
                exit()
    logging.info('Individual column: {}'.format(id))
    if id not in class_vec:
        logging.info('The initial letter of {} should be capital'.format(id))
        exit()
    id_in_data = list(data_df[id])
    if len(set(id_in_data)) != len(id_in_data):
        logging.info('Duplicated ids exit in the data file, please check!')
        exit()
    id_in_gmat = list(pd.read_csv(gmat_file + '.id', sep='\s+', header=None, dtype={0: 'str'}).iloc[:, 0])
    ind_keep = []
    for val in data_df[id]:
        if val in id_in_gmat:
            ind_keep.append(True)
        else:
            ind_keep.append(False)
    data_df = data_df.iloc[ind_keep, :]
    logging.info('Trait column name: {}'.format(trait))
    if len(set(trait) & set(class_vec)) != 0:
        logging.info('Phenotype should not be defined as class variable, please check!')
        exit()
    logging.info("The genomic relationship matrix file is: {}.agrm.id_fmt".format(gmat_file))
    id_dct = dict(zip(id_in_data, range(len(id_in_data))))
    ag = np.zeros((len(id_in_data), len(id_in_data)))
    with open(gmat_file + '.agrm.id_fmt') as fin:
        for line in fin:
            arr = line.split()
            try:
                ag[id_dct[arr[0]], id_dct[arr[1]]] = ag[id_dct[arr[1]], id_dct[arr[0]]] = float(arr[2])
            except Exception as e:
                del e
    logging.info('***Eigen decomposition of kinship matrix***')
    ag_eigen_val, ag_eigen_vec = linalg.eigh(ag)
    logging.info('***Build the design matrix for fixed effect***')
    tmin = np.min(tpoint)
    tmax = np.max(tpoint)
    leg_fix = _leg_mt(np.array(tpoint), tmax, tmin, forder)
    xmat_bt = np.concatenate(leg_fix, axis=1)
    xmat_t = [xmat_bt] * data_df.shape[0]
    if tfix is not None:
        xmat_t = []
        dmat_t = _design_matrix(tfix, data_df)
        for i in range(dmat_t.shape[0]):
            mat = []
            for j in range(dmat_t.shape[1]):
                mat.append(xmat_bt * dmat_t[i, j])
            mat = np.concatenate(mat, axis=1)
            xmat_t.append(mat)
    xmat = np.concatenate(xmat_t, axis=0)
    if fix is not None:
        xmat_nt = []
        dmat_nt = _design_matrix(fix, data_df)
        for i in range(dmat_nt.shape[0]):
            mat = []
            for j in range(1, dmat_nt.shape[1]):
                mat.append(np.array([dmat_nt[i, j]] * len(tpoint)).reshape(-1, 1))
            mat = np.concatenate(mat, axis=1)
            xmat_nt.append(mat)
        xmat_nt = np.concatenate(xmat_nt, axis=0)
        xmat = np.concatenate([xmat, xmat_nt], axis=1)
    if np.linalg.matrix_rank(xmat) < xmat.shape[1]:
        xmat = _full_col_rank(xmat)
    xmat = np.dot(linalg.kron(ag_eigen_vec.T, np.eye(len(tpoint))), xmat)
    xmat = xmat.reshape(data_df.shape[0], len(tpoint), -1)
    logging.info('***Initial values for variances and rotate the phenotypic values')
    leg_tp = _leg_mt(np.array(tpoint), tmax, tmin, rorder)
    leg_tp = np.concatenate(leg_tp, axis=1)
    y = np.array(data_df[trait])
    cov_dim = leg_tp.shape[1]
    y_var = np.var(y) / (cov_dim * 2 + 1)
    var_com = []
    cov_var = np.diag([y_var] * cov_dim)
    var_com.extend(cov_var[np.tril_indices_from(cov_var)])
    var_com.extend(cov_var[np.tril_indices_from(cov_var)])
    var_com.append(y_var)
    if init is None:
        var_com = np.array(var_com)
    else:
        if len(var_com) != len(init):
            logging.info('The length of initial variances should be {}'.format(len(var_com)))
            exit()
        else:
            var_com = np.array(init)
    y = np.dot(ag_eigen_vec.T, y)
    y = y.reshape(data_df.shape[0], len(tpoint), 1)
    return y, xmat, leg_tp, var_com, ag_eigen_val
