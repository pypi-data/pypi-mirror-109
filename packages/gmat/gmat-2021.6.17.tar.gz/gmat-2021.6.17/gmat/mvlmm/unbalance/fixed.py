import sys
import math
import numpy as np
import pandas as pd
from scipy import linalg
from scipy import sparse
from scipy.stats import chi2
from scipy.sparse import csr_matrix, block_diag, bmat
import logging
from tqdm import tqdm
from functools import reduce
from gmat.process_plink.process_plink import impute_geno
from pysnptools.snpreader import Bed


from gmat.mvlmm.unbalance._pre_data import _pre_data


def fixed(data_file, id, trait, bed_file, agmat_file, var_com, snp_lst=None, fix=None, prefix_outfile='fixed'):
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
    y_lst, xmat_lst, zmat_lst, ag, error_lst, id_raw_lst = _pre_data(data_file, id, trait, agmat_file, fix=fix)
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
    add_cov, error_cov = pre_cov(y_lst, var_com)
    xmat_con = np.array(xmat_lst[0])
    for i in range(1, len(xmat_lst)):
        xmat_con = linalg.block_diag(xmat_con, xmat_lst[i])
    zmat_con = block_diag(zmat_lst, format='csr')
    y_con = np.concatenate(y_lst, axis=0)
    vmat = []
    for i in range(len(error_lst)):
        vec = []
        for j in range(len(error_lst[i])):
            vec.append(error_lst[i][j] * error_cov[i, j])
        vmat.append(vec)
    vmat = bmat(vmat, format='csr')
    vmat += zmat_con.dot((zmat_con.dot(linalg.kron(add_cov, ag))).T)
    vmat = linalg.inv(vmat)
    vxmat = np.dot(vmat, xmat_con)
    xvxmat = np.dot(xmat_con.T, vxmat)
    xvxmat = linalg.inv(xvxmat)
    pmat = vmat - reduce(np.dot, [vxmat, xvxmat, vxmat.T])
    snp_on_disk = Bed(bed_file, count_A1=False)
    fam_df = pd.read_csv(bed_file + '.fam', sep='\s+', header=None)
    id_geno = list(np.array(fam_df.iloc[:, 1], dtype=str))
    id_order_index = []
    for i in id_raw_lst:
        id_order_index.append(id_geno.index(i))
    logging.info('***Read the snp data***')
    num_id = snp_on_disk.iid_count
    num_snp = snp_on_disk.sid_count
    logging.info("There are {:d} individuals and {:d} SNPs.".format(num_id, num_snp))
    if snp_lst is None:
        snp_lst = range(num_snp)
    snp_lst = list(snp_lst)
    if min(snp_lst) < 0 or max(snp_lst) >= num_snp:
        logging.info('The value in the snp list should be >= {} and < {}', 0, num_snp)
        exit()
    snp_mat = snp_on_disk[:, snp_lst].read().val
    if np.any(np.isnan(snp_mat)):
        logging.info('Missing genotypes are imputed with random genotypes.')
        snp_mat = impute_geno(snp_mat)
    bye_mat = np.zeros((len(id_raw_lst), len(y_lst)-1))
    indexa = len(y_lst[0])
    for i in range(1, len(y_lst)):
        indexb = indexa + len(y_lst[i])
        bye_mat[indexa:indexb, i-1] = 1.0
        indexa = indexb
    logging.info('########################################################')
    logging.info('###Start the fixed regression GWAS for unbalance data###')
    logging.info('########################################################')
    chi_df = len(y_lst)
    eff_main_vec = []
    se_main_vec = []
    p_main_vec = []
    eff_vec = []
    p_gbye_vec = []
    p_vec = []
    for i in tqdm(range(snp_mat.shape[1])):
        snp_fix = snp_mat[id_order_index, i:(i+1)]
        p_xsnp = np.dot(pmat, snp_fix)
        xpx = np.dot(snp_fix.T, p_xsnp)
        se_main = np.sqrt(xpx[0, 0])
        xpy = np.dot(p_xsnp.T, y_con)
        eff_main = xpy[-1, -1]
        chi_val = eff_main*eff_main/(se_main*se_main)
        p_main = chi2.sf(chi_val, 1)
        eff_main_vec.append(eff_main)
        se_main_vec.append(se_main)
        p_main_vec.append(p_main)
        snp_fix = np.concatenate([snp_fix, snp_fix*bye_mat], axis=1)
        p_xsnp = np.dot(pmat, snp_fix)
        xpx = np.dot(snp_fix.T, p_xsnp)
        xpx = linalg.inv(xpx)
        xpy = np.dot(p_xsnp.T, y_con)
        b = np.dot(xpx, xpy)
        eff = b[-(chi_df-1):, -1]
        eff_var = xpx[-(chi_df-1):, -(chi_df-1):]
        chi_val = np.sum(np.dot(np.dot(eff.T, linalg.inv(eff_var)), eff))
        p_gbye = chi2.sf(chi_val, chi_df-1)
        p_gbye_vec.append(p_gbye)
        eff = b[-chi_df:, -1]
        eff_var = xpx[-chi_df:, -chi_df:]
        chi_val = np.sum(np.dot(np.dot(eff.T, linalg.inv(eff_var)), eff))
        p_val = chi2.sf(chi_val, chi_df)
        eff_vec.append(eff)
        p_vec.append(p_val)
    logging.info('Finish association analysis')
    logging.info('***Output***')
    snp_info_file = bed_file + '.bim'
    snp_info = pd.read_csv(snp_info_file, sep='\s+', header=None)
    res_df = snp_info.iloc[snp_lst, [0, 1, 3, 4, 5]]
    res_df.columns = ['chro', 'snp_ID', 'pos', 'allele1', 'allele2']
    res_df.loc[:, 'order'] = snp_lst
    res_df = res_df.iloc[:, [5, 0, 1, 2, 3, 4]]
    res_df.loc[:, 'eff_main'] = eff_main_vec
    res_df.loc[:, 'se_main'] = se_main_vec
    res_df.loc[:, 'p_main'] = p_main_vec
    eff_vec = np.array(eff_vec)
    for i in range(eff_vec.shape[1]):
        col_ind = 'eff' + str(i)
        res_df.loc[:, col_ind] = eff_vec[:, i]
    res_df.loc[:, 'p_gbye'] = p_gbye_vec
    res_df.loc[:, 'p_val'] = p_vec
    out_file = prefix_outfile + '.res'
    res_df.to_csv(out_file, sep='\t', index=False)
    return res_df










