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

    # optimaze philips infiltratoin
    # stores ks and s into .philip file
    # get_ks_s(OD.data, pars.out_dir)

    DE = DiffEvol(pars = pars, obs = OD)
    DE.make_de()

if __name__ == '__main__':

    main(read_parser())
