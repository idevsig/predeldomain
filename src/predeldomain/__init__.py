import argparse
import sys

from predeldomain.app.entry import entry


def parse_arguments():
    parser = argparse.ArgumentParser(description='The domain to be pre-deleted.')

    parser.add_argument(
        '-l',
        '--length',
        type=int,
        default=3,
        metavar='[1-10]',
        choices=range(1, 11),
        help='Length: 1 to 10',
    )
    parser.add_argument(
        '-m',
        '--mode',
        type=int,
        choices=[1, 2, 3],
        default=1,
        help='Mode: 1. Alphanumeric, 2. Numeric, 3. Alphabetic',
    )
    parser.add_argument(
        '-s',
        '--suffix',
        type=str,
        choices=['cn', 'top'],
        default='cn',
        help="Suffix: 'cn' or 'top'",
    )
    parser.add_argument(
        '-t',
        '--type',
        type=str,
        choices=['text', 'json'],
        default='text',
        help="Save type: 'text' or 'json'",
    )
    parser.add_argument(
        '-w',
        '--whois',
        type=str,
        default='',
        help='Whois: whois, isp, none',
    )

    args = parser.parse_args()
    return args


def main():
    try:
        args = parse_arguments()
        entry(args)

    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)
