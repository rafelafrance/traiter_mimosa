#!/usr/bin/env python3
"""Clean text to prepare it for trait extraction."""
import argparse
import logging
import textwrap
from pathlib import Path

import ftfy
import regex as re
from traiter import log

MOJIBAKE = {
    "{": "(",
    "}": ")",
}


def main():
    """Clean the text."""
    args = parse_args()
    log.started()
    clean(args)
    log.finished()


def clean(args):
    """Clean text to prepare it for trait extraction."""
    with open(args.in_text) as raw_file:
        text = raw_file.read()

    # The bulk of the text cleaning happens in this function
    logging.info("Cleaning text")
    trans = str.maketrans(MOJIBAKE)
    text = clean_text(text, trans=trans)

    with open(args.out_text, "w") as clean_file:
        clean_file.write(text)


def clean_text(
    text: str,
    trans: dict[int, str] = None,
) -> str:
    text = text if text else ""

    # Handle uncommon mojibake
    text = text.translate(trans)

    text = " ".join(text.split())  # Space normalize

    # Join hyphenated words when they are at the end of a line
    text = re.sub(r"([a-z])-\s+([a-z])", r"\1\2", text, flags=re.IGNORECASE)

    text = ftfy.fix_text(text)  # Handle common mojibake

    text = re.sub(r"\p{Cc}+", " ", text)  # Remove control characters

    return text


def parse_args():
    """Process command-line arguments."""
    description = """Clean text to prepare it for trait extraction."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--in-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Which text file to clean.""",
    )

    arg_parser.add_argument(
        "--out-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the cleaned text to this file.""",
    )

    arg_parser.add_argument(
        "--nlp-max-length",
        type=int,
        default=5,
        metavar="MB",
        help="""The maximum text file size to process. This is given in megabytes.
            This is a spaCy constraint. (default: %(default)s)""",
    )

    args = arg_parser.parse_args()
    args.nlp_max_length *= 1_000_000
    return args


if __name__ == "__main__":
    main()
