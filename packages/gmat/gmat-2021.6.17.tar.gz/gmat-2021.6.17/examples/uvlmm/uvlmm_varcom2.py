import logging
from gmat.gmatrix import agmat
from gmat.uvlmm.gwas import fixed, fixed_gbye
from gmat.uvlmm.varcom import weight_emai_eigen


logging.basicConfig(level=logging.INFO)
pheno_file = 'pheno'
bed_file = 'plink'


agmat_file = 'test'
agmat2 = agmat(bed_file, out_file=agmat_file, inv=False, small_val=0.001, out_fmt='id_id_val')

weight_emai_eigen(pheno_file, agmat_file, class_lst=["mean", "sex", "treat"], \
fix="mean + sex + age + treat", maxiter0=100)
