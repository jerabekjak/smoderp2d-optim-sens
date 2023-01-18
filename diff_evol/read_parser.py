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
        help='directory to store the optimaze results [default: out-test]',
        type=str,
        default='out-test',
        required=False
    )

    parser.add_argument(
        '-m',
        '--mod_conf',
        help='location of model config file [default: model/test.ini]',
        type=str,
        default='model/test.ini',
        required=False
    )

    parser.add_argument(
        '-O',
        '--opt_conf',
        help='location of optimization config file [default: optim.cfg]',
        type=str,
        default='optim.cfg',
        required=False
    )

    parser.add_argument(
        '-T',
        '--texture',
        help='what is the soil texture?',
        type=str,
        default='NA',
        required=False
    )

    return parser.parse_args()
