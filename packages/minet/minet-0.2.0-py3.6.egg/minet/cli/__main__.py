#!/usr/bin/env python
# =============================================================================
# Minet CLI Endpoint
# =============================================================================
#
# CLI enpoint of the Minet library.
#
import csv
import sys
import shutil
from textwrap import dedent
from argparse import ArgumentParser, FileType, RawTextHelpFormatter

from minet.cli.defaults import DEFAULT_CONTENT_FOLDER

SUBPARSERS = {}

terminal_size = shutil.get_terminal_size()
csv.field_size_limit(sys.maxsize)

def custom_formatter(prog):
    return RawTextHelpFormatter(
        prog,
        max_help_position=50,
        width=terminal_size.columns,
    )


def main():
    parser = ArgumentParser(prog='minet')
    subparsers = parser.add_subparsers(
        help='action to execute', title='actions', dest='action')

    # Fetch action subparser
    fetch_description = dedent(
        '''
        Minet Fetch Command
        ===================

        Use multiple threads to fetch batches of urls from a CSV file. The
        command outputs a CSV report with additional metadata about the
        HTTP calls and will generally write the retrieved files in a folder
        given by the user.
        '''
    )

    fetch_epilog = dedent(
        '''
        examples:

        . Fetching a batch of url from existing CSV file:
            `minet fetch url_column file.csv > report.csv`

        . CSV input from stdin:
            `xsv select url_column file.csv | minet fetch url_column > report.csv`

        . Fetching a single url, useful to pipe into `minet scrape`:
            `minet fetch http://google.com | minet scrape ./scrape.json > scraped.csv`
        '''
    )

    fetch_subparser = subparsers.add_parser(
        'fetch',
        description=fetch_description,
        epilog=fetch_epilog,
        formatter_class=custom_formatter
    )

    fetch_subparser.add_argument(
        'column',
        help='Column of the CSV file containing urls to fetch.'
    )

    fetch_subparser.add_argument(
        'file',
        help='CSV file containing the urls to fetch.',
        type=FileType('r'),
        default=sys.stdin,
        nargs='?'
    )

    fetch_subparser.add_argument(
        '--contents-in-report',
        help='Whether to include retrieved contents, e.g. html, directly in the report\nand avoid writing them in a separate folder. This requires to standardize\nencoding and won\'t work on binary formats.',
        action='store_true'
    )
    fetch_subparser.add_argument(
        '-d', '--output-dir',
        help='Directory where the fetched files will be written. Defaults to "%s".' % DEFAULT_CONTENT_FOLDER,
        default=DEFAULT_CONTENT_FOLDER
    )
    fetch_subparser.add_argument(
        '-f', '--filename',
        help='Name of the column used to build retrieved file names. Defaults to an uuid v4 with correct extension.'
    )
    fetch_subparser.add_argument(
        '--filename-template',
        help='A template for the name of the fetched files.'
    )
    fetch_subparser.add_argument(
        '-g', '--grab-cookies',
        help='Whether to attempt to grab cookies from your computer\'s chrome browser.',
        action='store_true'
    )
    fetch_subparser.add_argument(
        '--standardize-encoding',
        help='Whether to systematically convert retrieved text to UTF-8.',
        action='store_true'
    )
    fetch_subparser.add_argument(
        '-o', '--output',
        help='Path to the output report file. By default, the report will be printed to stdout.'
    )
    fetch_subparser.add_argument(
        '-s', '--select',
        help='Columns to include in report (separated by `,`).'
    )
    fetch_subparser.add_argument(
        '-t', '--threads',
        help='Number of threads to use. Defaults to 25.',
        type=int,
        default=25
    )
    fetch_subparser.add_argument(
        '--throttle',
        help='Time to wait - in seconds - between 2 calls to the same domain. Defaults to 0.2.',
        type=float,
        default=0.2
    )
    fetch_subparser.add_argument(
        '--total',
        help='Total number of lines in CSV file. Necessary if you want to display a finite progress indicator.',
        type=int
    )
    fetch_subparser.add_argument(
        '--url-template',
        help='A template for the urls to fetch. Handy e.g. if you need to build urls from ids etc.'
    )

    # TODO: lru_cache, normalize urls, print current urls? print end report?

    SUBPARSERS['fetch'] = fetch_subparser

    # Extract action subparser
    extract_description = dedent(
        '''
        Minet Extract Command
        =====================

        Use multiple processes to extract raw text from a batch of HTML files.
        This command can either work on a `minet fetch` report or on a bunch
        of files. It will output an augmented report with the extracted text.
        '''
    )

    extract_epilog = dedent(
        '''
        examples:

        . Extracting raw text from a `minet fetch` report:
            `minet extract report.csv > extracted.csv`

        . Working on a report from stdin:
            `minet fetch url_column file.csv | minet extract > extracted.csv`

        . Extracting raw text from a bunch of files:
            `minet extract --glob "./content/*.html" > extracted.csv`
        '''
    )

    extract_subparser = subparsers.add_parser(
        'extract',
        description=extract_description,
        epilog=extract_epilog,
        formatter_class=custom_formatter
    )

    extract_subparser.add_argument(
        'report',
        help='Input CSV fetch action report file.',
        type=FileType('r'),
        default=sys.stdin,
        nargs='?'
    )

    extract_subparser.add_argument(
        '-e', '--extractor',
        help='Extraction engine to use. Defaults to `dragnet`.',
        choices=['dragnet', 'html2text']
    )
    extract_subparser.add_argument(
        '-i', '--input-directory',
        help='Directory where the HTML files are stored. Defaults to "%s".' % DEFAULT_CONTENT_FOLDER,
        default=DEFAULT_CONTENT_FOLDER
    )
    extract_subparser.add_argument(
        '-o', '--output',
        help='Path to the output report file. By default, the report will be printed to stdout.'
    )
    extract_subparser.add_argument(
        '-p', '--processes',
        help='Number of processes to use. Defaults to 4.',
        type=int,
        default=4
    )
    extract_subparser.add_argument(
        '-s', '--select',
        help='Columns to include in report (separated by `,`).'
    )
    extract_subparser.add_argument(
        '--total',
        help='Total number of HTML documents. Necessary if you want to display a finite progress indicator.',
        type=int
    )

    SUBPARSERS['extract'] = extract_subparser

    # Scrape action subparser
    scrape_description = dedent(
        '''
        Minet Scrape Command
        ====================

        Use multiple processes to scrape data from a batch of HTML files.
        This command can either work on a `minet fetch` report or on a bunch
        of files. It will output the scraped items.
        '''
    )

    scrape_epilog = dedent(
        '''
        examples:

        . Scraping item from a `minet fetch` report:
            `minet scrape scraper.json report.csv > scraped.csv`

        . Working on a report from stdin:
            `minet fetch url_column file.csv | minet fetch scraper.json > scraped.csv`

        . Scraping items from a bunch of files:
            `minet scrape scraper.json --glob "./content/*.html" > scraped.csv`
        '''
    )

    scrape_subparser = subparsers.add_parser(
        'scrape',
        description=scrape_description,
        epilog=scrape_epilog,
        formatter_class=custom_formatter
    )

    scrape_subparser.add_argument(
        'scraper',
        help='Path to a scraper definition file.',
        type=FileType('r')
    )

    scrape_subparser.add_argument(
        'report',
        help='Input CSV fetch action report file.',
        type=FileType('r'),
        default=sys.stdin,
        nargs='?'
    )

    scrape_subparser.add_argument(
        '-i', '--input-directory',
        help='Directory where the HTML files are stored. Defaults to "%s".' % DEFAULT_CONTENT_FOLDER,
        default=DEFAULT_CONTENT_FOLDER
    )
    scrape_subparser.add_argument(
        '-o', '--output',
        help='Path to the output report file. By default, the report will be printed to stdout.'
    )
    scrape_subparser.add_argument(
        '-p', '--processes',
        help='Number of processes to use. Defaults to 4.',
        type=int,
        default=4
    )
    scrape_subparser.add_argument(
        '--total',
        help='Total number of HTML documents. Necessary if you want to display a finite progress indicator.',
        type=int
    )

    SUBPARSERS['scrape'] = scrape_subparser

    help_suparser = subparsers.add_parser('help')
    help_suparser.add_argument('subcommand', help='name of the subcommand')
    SUBPARSERS['help'] = help_suparser

    args = parser.parse_args()

    if args.action == 'help':
        target_subparser = SUBPARSERS.get(args.subcommand)

        if target_subparser is None:
            parser.print_help()
        else:
            target_subparser.print_help()

    elif args.action == 'fetch':
        from minet.cli.fetch import fetch_action
        fetch_action(args)

    elif args.action == 'extract':
        try:
            import dragnet
        except:
            print('The `dragnet` library is not installed. The `extract` command won\'t work.')
            print('To install it correctly, run the following commands in order:')
            print()
            print('  pip install lxml numpy Cython')
            print('  pip install dragnet')
            sys.exit(1)

        from minet.cli.extract import extract_action
        extract_action(args)

    elif args.action == 'scrape':
        from minet.cli.scrape import scrape_action
        scrape_action(args)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
