import argparse


def read_parser():
    parser = argparse.ArgumentParser(
        description='Run Smoderp2D optimalization with differential evolution.')


    parser.add_argument(
        '-out_dir',
        help='directory to store the results',
        type=str,
        default='out-test',
        required=False
    )

    parser.add_argument(
        '-mod_conf',
        help='location of model config file',
        type=str,
        required=False
    )
    
    parser.add_argument(
        '-obs_data',
        help='location of observed data',
        type=str,
        default='obs_data/data.dat',
        required=False
    )
    
    return parser.parse_args()
