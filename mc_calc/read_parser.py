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
        help='location of sens. analysis config file [default: sens.cfg]',
        type=str,
        default='sens.cfg',
        required=False
    )

    parser.add_argument(
        '-m',
        '--mod_conf',
        help='location of model ini file  [default: model/test.ini]',
        type=str,
        default='model/test.ini',
        required=False
    )

    parser.add_argument(
        '-o',
        '--out_dir',
        help='directory to store the results [default: out-test-sens]',
        type=str,
        default='out-test-sens',
        required=False
    )

    return parser.parse_args()
