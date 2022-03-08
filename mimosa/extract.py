#!/usr/bin/env python3
"""Parse efloras treatments."""
import argparse
import textwrap
from pathlib import Path

from pylib.readers import mimosa_reader
from pylib.writers import html_writer


def main():
    """Perform actions based on the arguments."""
    args = parse_args()
    data = mimosa_reader.read(args)
    html_writer.write(args, data)


def parse_args():
    """Process command-line arguments."""
    description = """Parse data about mimosas from PDFs converted into text files."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--in-text",
        type=Path,
        metavar="PATH",
        help="""Which text file (a converted PDF) to process.""",
    )

    arg_parser.add_argument(
        "--out-html",
        type=Path,
        metavar="PATH",
        help="""Output the results to this HTML file.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
