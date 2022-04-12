#!/usr/bin/env python3
"""Clean text to prepare it for trait extraction."""
import argparse
import logging
import textwrap
from pathlib import Path

from pylib.pipelines import sentence_pipeline
from traiter import log
from traiter import util as t_util

MOJIBAKE = {
    "{": "(",
    "}": ")",
}


def main():
    """Clean the text."""
    args = parse_args()

    log.started()

    clean_text(args)

    log.finished()


def clean_text(args):
    """Clean text to prepare it for trait extraction."""
    with open(args.in_text) as raw_file:
        text = raw_file.read()

    # The bulk of the text cleaning happens in this external function
    logging.info("Cleaning text")
    trans = str.maketrans(MOJIBAKE)
    text = t_util.clean_text(text, trans=trans)

    # Break into sentences
    logging.info("Breaking text into sentences")
    nlp = sentence_pipeline.pipeline()
    nlp.max_length = args.nlp_max_length
    doc = nlp(text)

    # Write output
    lines = [s.text + "\n" for s in doc.sents if s and s.text]
    with open(args.out_text, "w") as clean_file:
        clean_file.writelines(lines)


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
