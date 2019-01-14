#!/usr/bin/python3

import argparse

def main(pars):
    
    pass
    


def init() :
    parser = argparse.ArgumentParser(description='Run Smoderp2D.')

    # type of computation
    parser.add_argument(
        '-obs_data',
        help='location of observed data',
        type=str,
        required=True
    )

    # data file (only required for runoff)
    parser.add_argument(
        '-outputdir',
        help='directory to store the ',
        type=str,
        required=True
    )
    return parser.parse_args()

if __name__ == '__main__' : 
    
    
    main (init())
