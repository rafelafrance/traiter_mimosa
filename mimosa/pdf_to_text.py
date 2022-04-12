#!/usr/bin/env python3
"""Convert a PDF into text directly."""
import argparse
import os
import textwrap
from pathlib import Path

import rich


def main():
    """Convert the file."""
    args = parse_args()

    pdf_to_text(args)

    msg = " ".join(
        """You may want to remove headers, footers,
        figure captions (& text), map captions (& text), etc.
        from this text file.""".split()
    )
    rich.print(f"\n[bold yellow]{msg}[/bold yellow]\n")


def pdf_to_text(args):
    """Convert the PDF to text."""
    text_file = args.text_dir / args.in_pdf.name
    text_file = text_file.with_suffix(".txt")
    os.system(f"pdftotext {args.in_pdf} {text_file}")


def parse_args():
    """Process command-line arguments."""
    description = """Sometimes you can convert a PDF directly to text with great
        results, and sometimes not. Look at the output of this conversion to see if
        the output is acceptable."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--in-pdf",
        type=Path,
        required=True,
        metavar="PDF",
        help="""Which pdf file to convert to text.""",
    )

    arg_parser.add_argument(
        "--text-dir",
        type=Path,
        required=True,
        metavar="DIR",
        help="""Where to place the text file.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
