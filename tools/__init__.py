import argparse
import textwrap

def read_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
         Optimize smoderp2d with differential evolution.
         -----------------------------------------------
         '''))

    parser.add_argument(
        '-o',
        '--out_dir',
        help='directory to store the results',
        type=str,
        default='out-test',
        required=False
    )

    parser.add_argument(
        '-m',
        '--mod_conf',
        help='location of model config file',
        type=str,
        default='model/test.ini',
        required=False
    )

    parser.add_argument(
        '-O',
        '--opt_conf',
        help='location of optimization config file',
        type=str,
        default='optim.cfg',
        required=False
    )

    return parser.parse_args()
