import argparse

from .differs import MD5Differ
from .requester import Requester
from .curl import CurlDataGetter
from .actions import print_results, print_scrapy_request


differs = {
    'md5': MD5Differ
}

actions = {
    'print_results': print_results,
    'print_scrapy_request': print_scrapy_request
}


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--differ',
        help="Mode to use for diffing responses",
        choices=['md5'],
        default='md5'
    )

    parser.add_argument(
        '--action',
        help="Choose action to do with the results",
        choices=actions.keys(),
        default='print_results'
    )

    parser.add_argument(
        '--debug',
        help="Enable debugging messages",
        action='store_true'
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    differ = differs[args.differ]
    action = actions[args.action]
    curl_request = raw_input()

    cr = CurlDataGetter(curl_request)
    curl_data = cr.get_data()

    requester = Requester(curl_data=curl_data, differ=differ, debug=args.debug)
    results = requester.get_results_from_comparison()

    print '\n'
    action(results)
