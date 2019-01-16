#!/usr/bin/python3

from sens_ana.obs_data_handler import ObsData
from philip_optim import get_ks_s
from sens_ana.read_parser import read_parser
from sens_ana import SensAna
import os


def main(pars):

    # load observation data
    OD = ObsData(pars.sens_conf)
    if not os.path.exists(pars.out_dir):
        os.makedirs(pars.out_dir)

    # optimaze philips infiltratoin
    # stores ks and s into .philip file
    get_ks_s(OD.data, pars.out_dir)

    SA = SensAna(pars=pars, obs=OD)
    SA.do_sa()


if __name__ == '__main__':

    main(read_parser())
