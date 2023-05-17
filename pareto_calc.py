#!/usr/bin/python2

#from sens_ana.read_parser import read_parser
#from diff_evol.read_parser import read_parser
#from sens_ana.read_cfg import ReadConfig
#from diff_evol.obs_data_handler import ObsData
from pareto_calc import ParetoCalc
from sens_ana.obs_data_handler import ObsData
from diff_evol import DiffEvol
from philip_optim import get_ks_s
from diff_evol.read_parser import read_parser
import os


def main(pars):
    """ Perform one at the time optimization based on Morris, 1991 """

    #BF_sens = ReadConfig(pars.sens_conf)
    OD = ObsData(pars.opt_conf)
    
    if not os.path.exists(pars.out_dir):
        os.makedirs(pars.out_dir)

    SA = ParetoCalc(pars=pars, cfgs=OD)
    SA.do_sa()


if __name__ == '__main__':

    main(read_parser())
