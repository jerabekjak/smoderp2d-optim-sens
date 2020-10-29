#!/usr/bin/python3

from diff_evol.obs_data_handler import ObsData
from recalc_pareto import RecalcPareto
from philip_optim import get_ks_s
from diff_evol.read_parser import read_parser
from tools.writes import write_de
import os
import numpy
import shutil
def main(pars):

    # load observation data
    OD = ObsData(pars.opt_conf)
    
    if not os.path.exists(pars.out_dir):
        os.makedirs(pars.out_dir)
    RP = RecalcPareto(pars = pars, obs = OD)

    counter = 1
    for par in RP.pars_matrix:
        RP.model(numpy.array(par))
        new_pth = '{}.{}'.format(pars.out_dir, str(counter).zfill(3))
        print (new_pth)
        if os.path.exists(new_pth):
            shutil.rmtree(new_pth)
        shutil.copytree(pars.out_dir, new_pth)
        counter += 1
        write_de(RP._obs, 
                RP._mod_data_h_interp,
                RP._mod_data_q_interp,
                RP.result, new_pth)

    
    print ('111111111111111111111111')
if __name__ == '__main__':

    main(read_parser())
