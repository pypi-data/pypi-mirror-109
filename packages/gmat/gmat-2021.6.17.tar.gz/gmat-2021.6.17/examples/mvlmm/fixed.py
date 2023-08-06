import numpy as np
import pandas as pd
from gmat.gmatrix import agmat
from gmat.mvlmm.unbalance import fixed
import logging
logging.basicConfig(level=logging.INFO)

bed_file = '/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/yeast/CobaltChloride'


data_file = '/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/yeast/CobaltChloride12'
id = 'ID'
trait = ['trait1', 'trait2']
agmat_file = '/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/yeast/test'
var_com = pd.read_csv("/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/yeast/mvlmm_varcom.var", sep='\s+', header=0)
prefix_outfile = '/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/yeast/fixed3.res'
fixed(data_file, id, trait, bed_file, agmat_file, var_com, snp_lst=None, fix=None, prefix_outfile=prefix_outfile)
