import numpy as np
import pandas as pd
from gmat.gmatrix import agmat
from gmat.mvlmm.unbalance import varcom
import logging
logging.basicConfig(level=logging.INFO)

bed_file = '/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/yeast/CobaltChloride'
agmat(bed_file, out_file='/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/yeast/test', out_fmt='id_id_val')

data_file = '/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/yeast/CobaltChloride12'
id = 'ID'
trait = ['trait1', 'trait2']
agmat_file = '/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/yeast/test'
varcom(data_file, id, trait, agmat_file, fix=None, init=None, maxiter=100, 
cc_par=1e-08, cc_gra=0.001, em_weight_step=0.01,
       prefix_outfile='/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/yeast/mvlmm_varcom')



