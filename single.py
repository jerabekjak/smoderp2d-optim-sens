#!/usr/bin/python3

from diff_evol.obs_data_handler import ObsData
from diff_evol import DiffEvol
from philip_optim import get_ks_s
from diff_evol.read_parser import read_parser
import os

def main(pars):

    # load observation data
    OD = ObsData(pars.opt_conf)
    
    if not os.path.exists(pars.out_dir):
        os.makedirs(pars.out_dir)
        
    get_ks_s(OD.data, pars.out_dir)
        
    DE = DiffEvol(pars = pars, obs = OD)
    DE.model([4.5,0.79,1.3,4.7e-06,2.6e-05,-0.00025])
    
if __name__ == '__main__':

    main(read_parser())
