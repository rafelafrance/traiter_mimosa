#!/usr/bin/env python3
"""Parse efloras treatments."""
import argparse
import textwrap
from pathlib import Path

from pylib.readers import mimosa_reader


def main():
    """Perform actions based on the arguments."""
    args = parse_args()
    mimosa_reader.read(args)


def parse_args():
    """Process command-line arguments."""
    description = """Parse data about mimosas from PDFs converted into text files."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--text-file",
        type=Path,
        help="""Which text file (a converted PDF) to process.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
