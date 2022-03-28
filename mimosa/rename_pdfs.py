#!/usr/bin/env python3
"""Rename ugly file names."""
import argparse
import shutil
import textwrap
from pathlib import Path

import regex as re


def main():
    """Convert the file."""
    args = parse_args()
    rename_files(args)


def rename_files(args):
    """Rename the PDFs."""
    for old_path in args.pdf_dir.glob("*.pdf"):
        print(f"Old name: {old_path}")

        stem = old_path.stem
        stem = re.sub(r"[^\w.]", "_", stem)
        stem = re.sub(r"__+", "_", stem)
        stem = re.sub(r"_+$", "", stem)

        new_path = old_path.with_stem(stem)

        if new_path == old_path:
            print("Not changed.")
        else:
            print(f"New name: {new_path}")
            shutil.move(old_path, new_path)

        print()


def parse_args():
    """Process command-line arguments."""
    description = """It's easier, not required but much easier, to work with sane
        file names. Remove characters that cause command line utilities problems.
        Remove spaces, commas, parentheses, etc. and replace them with underscores _.
        """
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--pdf-dir",
        type=Path,
        metavar="DIR",
        help="""The PDF directory containing PDFs with ugly file names.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
