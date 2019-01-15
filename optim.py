#!/usr/bin/python3


from diff_evol.obs_data_handler import ObsData
from diff_evol import DiffEvol
from philip_optim import get_ks_s
from tools import read_parser


def main(pars):

    # load observation data
    OD = ObsData(pars.obs_data)

    # optimaze philips infiltratoin
    # stores ks and s into .philip file
    get_ks_s(OD.data)

    DE = DiffEvol(obs = OD, pars = pars)
    DE.model([1,1,1])

if __name__ == '__main__':

    main(read_parser())
