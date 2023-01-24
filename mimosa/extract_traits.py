#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from pylib import mimosa_reader
from pylib.writers.csv_writer import CsvWriter
from pylib.writers.html_writer import HtmlWriter


def main():
    args = parse_args()
    traits_in_text, traits_by_taxon = mimosa_reader.read(args)

    if args.out_csv:
        writer = CsvWriter(args.out_csv)
        writer.write(traits_by_taxon)

    if args.out_html:
        writer = HtmlWriter(args.out_html)
        writer.write(traits_in_text)


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
