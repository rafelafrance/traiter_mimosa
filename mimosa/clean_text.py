#!/usr/bin/env python3
import argparse
import logging
import textwrap
from pathlib import Path

import ftfy
import regex as re
from pylib import sentence_pipeline
from traiter import log

MOJIBAKE = {
    "{": "(",
    "}": ")",
}

MOJIBAKE_WORDS = {
    # "find", "replace"
    r"Ivd": "lvd",
    r"1vd": "lvd",
    r"If-": "lf-",
    r"1f-": "lf-",
    r"If\.": "lf.",
    r"1f\.": "lf.",
    r"(?<=[a-z])U": "ll",
    r"-\s?l\b": "-1",
    r"\bl\s?-": "1-",
    r"-\s?l\s?l\b": "-11",
    r"\bl\s?l\s?-": "11-",
    r"\bl\s?1\b": "11",
    r"\bm\sm\b": "mm",
    r"1obe": "lobe",
    r"1eave": "leave",
    r"1eaf": "leaf",
    r"I\.(?=\d)": "1.",
    r"l\.(?=\d)": "1.",
    r"1(?=[a-z][a-z])": "l",
    r"(?<=[a-z][a-z])1": "l",
    r"Unear": "Linear",
}

MOJIBAKE_REPLACE = {}


def main():
    """Clean the text."""
    args = parse_args()
    log.started()
    clean(args)
    log.finished()


def clean(args):
    with open(args.in_text) as raw_file:
        text = raw_file.read()

    # The bulk of the text cleaning happens in this function
    logging.info("Cleaning text")
    trans = str.maketrans(MOJIBAKE)
    text = clean_text(text, trans=trans)

    # Break into sentences
    logging.info("Breaking text into sentences")
    nlp = sentence_pipeline.pipeline()
    nlp.max_length = args.nlp_max_length
    doc = nlp(text)

    # Write output
    lines = [s.text + "\n" for s in doc.sents if s and s.text]
    with open(args.out_text, "w") as clean_file:
        clean_file.writelines(lines)


def clean_text(
    text: str,
    trans: dict[int, str] = None,
) -> str:
    text = text if text else ""

    text = text.translate(trans)  # Handle uncommon mojibake

    text = replace_patterns(text)  # Replace messed up words

    text = " ".join(text.split())  # Space normalize

    # Join hyphenated words when they are at the end of a line
    text = re.sub(r"([a-z])-\s+([a-z])", r"\1\2", text, flags=re.IGNORECASE)

    # Handle spaces between digits
    text = re.sub(r"(\d) (\d)", r"\1\2", text)

    text = ftfy.fix_text(text)  # Handle common mojibake

    text = re.sub(r"\p{Cc}+", " ", text)  # Remove control characters

    return text


def replace_patterns(text: str) -> str:
    replaces = []
    for i, (pattern, repl) in enumerate(MOJIBAKE_WORDS.items()):
        name = f"X{i:04d}"
        MOJIBAKE_REPLACE[name] = repl
        replaces.append(f"(?P<{name}>{pattern})")
    regexp = "|".join(replaces)

    text = re.sub(regexp, lambda m: MOJIBAKE_REPLACE[m.lastgroup], text)
    return text


def parse_args():
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
