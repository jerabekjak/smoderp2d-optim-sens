#!/usr/bin/python2

from sens_ana.read_parser import read_parser
from sens_ana.read_cfg import ReadConfig
from sens_ana import SensAna
import os


def main(pars):
    """ compute  experiments with previous paraneters and fitted Ks and S data """
    
    # uses sensitivity analysis cfgs
    BF_sens = ReadConfig(pars.sens_conf)

if __name__ == '__main__':

    main(read_parser())
