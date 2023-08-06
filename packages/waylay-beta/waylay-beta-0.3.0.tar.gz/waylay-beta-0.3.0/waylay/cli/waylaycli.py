"""Command line interface for the Waylay Python SDK."""

import argparse
import logging
import sys

from waylay import WaylayClient


def init_doc_parser(parser):
    """Initialize the parser for the `doc` command."""
    parser.add_argument(
        '-s', '--service', dest='doc_service', nargs='*',
        help='Filter services to document.', default=None
    )
    parser.add_argument(
        '-r', '--resource', dest='doc_resource', nargs='*',
        help='Filter resources to document.', default=None
    )
    parser.add_argument(
        '-l', '--link', dest='doc_link', nargs='*', help='Filter doc sites links.', default=None
    )


def init_srv_parser(parser):
    """Initialize the parser for the `service` command."""
    cmd_parsers = parser.add_subparsers(dest='srv_cmd')
    cmd_parsers.add_parser('list', help='List services.')


def main():
    """Start the waylaycli program."""
    logging.basicConfig()
    parser = argparse.ArgumentParser(
        prog='waylaycli', description='Command line interface to the Waylay Python SDK'
    )
    parser.add_argument(
        '-p', '--profile', dest='profile', nargs='?', help='Configuration profile.', default=None
    )
    cmd_parsers = parser.add_subparsers(dest='cmd')
    init_doc_parser(cmd_parsers.add_parser('doc', help='Generate SDK overview of services.'))
    init_srv_parser(cmd_parsers.add_parser('service', help='Services.'))

    args = parser.parse_args()

    def waylay_client():
        return WaylayClient.from_profile(args.profile)

    if args.cmd == 'doc':
        print(waylay_client().util.info.action_info_html(
            service=args.doc_service, resource=args.doc_resource, links=args.doc_link
        ))
        return
    if args.cmd == 'service' and args.srv_cmd == 'list':
        profile = f'profile "{args.profile}"' if args.profile else 'default profile'
        print(
            f'{"key":^10} '
            f'| {" url for "+profile:^35} '
            f'| description'
        )
        print('-' * 10 + '   ' + '-' * 35 + '   ' + '-' * 30)
        for srv in waylay_client().services:
            print(
                f'{srv.service_key:>10} '
                f'| {srv.root_url:<35} '
                f'| {srv.description}'
            )
        return
    parser.print_help()
