#!/usr/bin/env python3
"""Convert a PDF file to images of pages."""
import argparse
import os
import textwrap
from pathlib import Path


def main():
    """Convert the file."""
    args = parse_args()

    pdf_to_images(args)

    msg = " ".join(
        """You may now want to remove pages that
        do not contain useful traits.""".split()
    )
    print(f"\n{msg}\n")


def pdf_to_images(args):
    """Convert the file."""
    stem = args.pdf_file.stem
    dst = args.image_dir / stem

    os.system(f"mkdir -p {dst}")
    os.system(f"pdftocairo -jpeg {args.pdf_file} {dst}/{stem}")


def parse_args():
    """Process command-line arguments."""
    description = """Convert a PDF file to images (jpg) of pages (one image per page).
        Note: This will create a subdirectory under the given image directory with
        a name that matches the PDF file name."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--pdf-file",
        type=Path,
        metavar="PDF",
        help="""Which pdf file to convert to images.""",
    )

    arg_parser.add_argument(
        "--image-dir",
        type=Path,
        metavar="DIR",
        help="""Where to place the images.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
