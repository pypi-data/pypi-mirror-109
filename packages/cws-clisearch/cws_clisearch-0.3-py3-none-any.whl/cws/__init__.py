"""CLI web search.

A CLI web search tool.
"""
import argparse
import sys
import subprocess
from signal import signal, SIGPIPE, SIG_DFL
from cws.config import cfg
from cws.cws import Cws
from cws.provider.searchprovider import SearchProvider


def list_providers():
    """List providers."""
    str = ''

    for provider in cfg.provider_yamls:
        provider = SearchProvider.from_yaml_file(
            cfg.provider_yamls[provider]
        )
        str += f"{provider.name}: {provider.token_url}\n"

    return str


def main():
    """Entry point and CLI argument parsing."""
    signal(SIGPIPE, SIG_DFL)

    if not cfg.token_file:
        print('No token config found, none of the engines will work. Bailing out.')
        return False

    parser = argparse.ArgumentParser(
        description='CLI web search tool.')

    parser.add_argument('search', type=str, nargs='?',
                        help='Seach query.')

    parser.add_argument('-p', '--provider',
                        help='The search provider to use.',
                        type=str, nargs='?',
                        default=cfg.userconfig['default_provider'],
                        choices=[i for i in cfg.provider_yamls])
    parser.add_argument('-n', '--number',
                        help='The number of results to show.',
                        type=int, nargs='?',
                        default=25)
    parser.add_argument('-u', '--url',
                        help='Show the urls only.',
                        action='store_true')
    parser.add_argument('-e', '--env',
                        type=str, nargs='?',
                        default='prod',
                        choices=['prod', 'dev'])
    parser.add_argument('-x', '--execute',
                        help='Execute default action of the provider on first result.',
                        action='store_true')
    parser.add_argument('--list-providers',
                        help='List available providers and the url to retrieve a token.',
                        action='store_true')

    (args, extra_args) = parser.parse_known_args()

    if not cfg.tokens[args.provider]:
        print('No tokens set up for this provider.')
        return False

    if args.execute:
        args.number = 1
        args.url = True

    cfg.env = args.env

    if args.list_providers:
        print(list_providers())
        exit(0)

    if not args.search:
        exit('Search arg is required.')

    cws = Cws(args.url, args.provider, args.search, args.number)
    results = cws.start_search()

    if args.execute:
        subprocess.Popen([cws.provider.default_action, str(results)], close_fds=True)
    else:
        for line in str(results).splitlines():
            sys.stdout.write(f"{line}\n")
        sys.stdout.write('\n')
