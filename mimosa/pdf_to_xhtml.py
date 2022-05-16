#!/usr/bin/env python3
import argparse
import os
import textwrap
from pathlib import Path

import rich


def main():
    args = parse_args()

    pdf_to_text(args)

    msg = " ".join(
        """You may want to remove headers, footers,
        figure captions (& text), map captions (& text), etc.
        from this text file.""".split()
    )
    rich.print(f"\n[bold yellow]{msg}[/bold yellow]\n")


def pdf_to_text(args):
    os.system(f"pdftotext -bbox -nodiag {args.in_pdf} {args.out_xhtml}")


def parse_args():
    description = """Convert a PDF to XHTML. The XHTML is not a web page, it has
        as special format that contains the bounding box of every word on every
        page."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--in-pdf",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Which pdf file to convert to HTML.""",
    )

    arg_parser.add_argument(
        "--out-xhtml",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the XHTML to this file.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
