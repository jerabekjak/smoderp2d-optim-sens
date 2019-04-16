#!/usr/bin/python2

from sens_ana.read_parser import read_parser
from sens_ana.read_cfg import ReadConfig
from valid_ana import ValidAna
import os


def main(pars):
    """ compute  experiments with previous paraneters and fitted Ks and S data """
    
    # uses sensitivity analysis cfgs
    VA_cfgs = ReadConfig(pars.sens_conf)
    
    # alter output dir_name
    pars.out_dir = pars.out_dir.replace('sens','valid')
    if not os.path.exists(pars.out_dir):
        os.makedirs(pars.out_dir)

    VA = ValidAna(pars=pars, cfgs=VA_cfgs)
    VA.do_va()

if __name__ == '__main__':

    main(read_parser())
