#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from pylib import mimosa_reader
from pylib.writers import csv_writer
from pylib.writers import html_writer


def main():
    args = parse_args()
    all_traits, taxa = mimosa_reader.read(args)

    if args.out_html:
        html_writer.write(args, all_traits)

    if args.out_csv:
        csv_writer.write(args, taxa)


def parse_args():
    description = """Parse data about mimosas from PDFs converted into text files."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--in-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Which text file (a converted PDF) to process.""",
    )

    arg_parser.add_argument(
        "--out-html",
        type=Path,
        metavar="PATH",
        help="""Output the results to this HTML file.""",
    )

    arg_parser.add_argument(
        "--out-csv",
        type=Path,
        metavar="PATH",
        help="""Output the results to this CSV file.""",
    )

    arg_parser.add_argument(
        "--limit",
        type=int,
        help="""Limit the input to this many records.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
