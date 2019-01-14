#!/usr/bin/python3

import argparse

from diff_evol.obs_data_handler import ObsData

def main(pars):
    
    # load observation data
    OD = ObsData(pars.obs_data)
    
def init() :
    parser = argparse.ArgumentParser(description='Run Smoderp2D.')

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

if __name__ == '__main__' : 
    
    
    main (init())
