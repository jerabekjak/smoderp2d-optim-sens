#!/usr/bin/python3

from diff_evol.obs_data_handler import ObsData
from diff_evol import DiffEvol
from philip_optim import get_ks_s
from diff_evol.read_parser import read_parser
import os
import numpy
def main(pars):

    # load observation data
    OD = ObsData(pars.opt_conf)
    
    if not os.path.exists(pars.out_dir):
        os.makedirs(pars.out_dir)
        
    #get_ks_s(OD.data, pars.out_dir)
        
    DE = DiffEvol(pars = pars, obs = OD)
    # vysledky.1/2/2018-05-31-risuty-157.log
    # nejlepsi nsh
    # params = numpy.array([9.8594, 1.4845, 1.0190, 3.8951e-08, 0.00044035, -1.7336e-03])
    # nejlepsi nsq
    # params = numpy.array([23.3550, 1.8210, 1.0189, 1.4811e-08, 0.00032817, -1.1557e-03])
    # kompromis nsq a nsh
    # params = numpy.array([23.4130, 1.8363, 1.0012, 1.0446e-08, 0.00035244, -3.1222e-03])
    params = numpy.array([3.6542e+01,3.0150e+00,1.2837e+00,7.9533e-07,1.0284e-04,-1.8243e-03])
    DE.model(params)
    
if __name__ == '__main__':

    main(read_parser())
