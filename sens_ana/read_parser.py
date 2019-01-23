import argparse
import textwrap


def read_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
         Sensitivity analysis of smoderp2d based on Morris 1991
         ------------------------------------------------------
         '''))

    parser.add_argument(
        '-O',
        '--sens_conf',
        help='location of sens. analysis config file',
        type=str,
        default='sens.cfg',
        required=False
    )

    parser.add_argument(
        '-o',
        '--out_dir',
        help='directory to store the results',
        type=str,
        default='out-test-sens',
        required=False
    )

    return parser.parse_args()
