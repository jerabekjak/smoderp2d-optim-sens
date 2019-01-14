#!/usr/bin/python3

import argparse

from diff_evol.obs_data_handler import ObsData
from diff_evol import DiffEvol
from philip_optim import get_ks_s


def main(pars):

    # load observation data
    OD = ObsData(pars.obs_data)

    # optimaze philips infiltratoin
    # stores ks and s into .philip file
    get_ks_s(OD.data)

    DE = DiffEvol(OD.data)


def init():
    parser = argparse.ArgumentParser(
        description='Run Smoderp2D optimalization with differential evolution.')

    parser.add_argument(
        '-obs_data',
        help='location of observed data',
        type=str,
        required=True
    )

    parser.add_argument(
        '-outputdir',
        help='directory to store the ',
        type=str,
        required=True
    )
    return parser.parse_args()


if __name__ == '__main__':

    main(init())
