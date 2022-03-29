#!/usr/bin/env python3
"""Clean text to prepare it for trait extraction."""
import argparse
import textwrap
from pathlib import Path

import traiter.util
from pylib.pipelines import sentence_pipeline as sp

MOJIBAKE = {
    "{": "(",
    "}": ")",
}
TRANS = str.maketrans(MOJIBAKE)


def main():
    """Clean the text."""
    args = parse_args()
    clean_text(args)


def clean_text(args):
    """Clean text to prepare it for trait extraction."""
    with open(args.input_text) as raw_file:
        text = raw_file.read()

    # The bulk of the text cleaning happens in this external function
    text = traiter.util.clean_text(text, trans=TRANS)

    # Break into sentences
    nlp = sp.pipeline()
    nlp.max_length = args.nlp_max_length
    doc = nlp(text)

    # Write output
    lines = [s.text + "\n" for s in doc.sents]
    with open(args.output_text, "w") as clean_file:
        clean_file.writelines(lines)


def parse_args():
    """Process command-line arguments."""
    description = """Clean text to prepare it for trait extraction."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--input-text",
        type=Path,
        metavar="PATH",
        help="""Which text file to clean.""",
    )

    arg_parser.add_argument(
        "--output-text",
        type=Path,
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
