#!/usr/bin/python3

from sens_ana.read_parser import read_parser
from sens_ana.read_cfg import ReadConfig
from sens_ana import SensAna
import os


def main(pars):
    """ Perform one at the time optimization based on Morris, 1991 """

    cfgs = ReadConfig(pars.sens_conf)

    if not os.path.exists(pars.out_dir):
        os.makedirs(pars.out_dir)

    #SA = SensAna(pars=pars)
    # SA.do_sa()


if __name__ == '__main__':

    main(read_parser())
