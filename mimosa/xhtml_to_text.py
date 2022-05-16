#!/usr/bin/env python3
import argparse
import textwrap
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

import rich
from bs4 import BeautifulSoup


@dataclass
class Word:
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    word: str


@dataclass
class Line:
    words: list[Word] = field(default_factory=list)

    @property
    def text(self):
        return " ".join(w.word for w in self.words)

    @property
    def top(self):
        return min(w.y_min for w in self.words)


@dataclass
class Page:
    no: int
    width: float
    height: float
    words: list[Word] = field(default_factory=list)
    lines: list[Line] = field(default_factory=list)


def main():
    args = parse_args()
    xhtml_to_text(args)

    msg = " ".join("""You may need to edit the output file manually.""".split())
    rich.print(f"\n[bold yellow]{msg}[/bold yellow]\n")


def xhtml_to_text(args):
    pages = read_html(args.in_xhtml, args.min_y, args.max_y)

    with open(args.out_text, "w") as out_text:
        for page in pages:
            lines = find_lines(page)
            page.lines = lines if args.gap_min < 1 else page_flow(args, page, lines)

            for ln in page.lines:
                print(ln.text, file=out_text)

            print(file=out_text)


def page_flow(args, page, lines):
    flow, col1, col2 = [], [], []
    center = page.width // 2
    gap_left = center - args.gap_radius
    gap_right = center + args.gap_radius
    for line in lines:
        split = find_column_split(line, args.gap_min, gap_left, gap_right)

        # Found a column gutter
        if split >= 0:
            col1.append(Line(line.words[:split]))
            col2.append(Line(line.words[split:]))

        # Found a left-side widow
        elif line.words[-1].x_max <= center:
            col1.append(line)

        # Found a right-side widow
        elif line.words[0].x_min >= center:
            col2.append(line)

        # This line spans both columns, so re-flow the columns
        else:
            flow += col1
            flow += col2
            flow.append(line)
            col1, col2 = [], []

    flow += col1
    flow += col2

    return flow


def find_column_split(line, gap_min, gap_left, gap_right):
    splits = []
    for i, (prev, curr) in enumerate(zip(line.words[:-1], line.words[1:]), 1):
        split = curr.x_min - prev.x_max
        x_min = max(prev.x_max, gap_left)
        x_max = min(curr.x_min, gap_right)
        inter = max(0.0, x_max - x_min)
        if split >= gap_min and inter > 0.0:
            splits.append((split, i))
    splits = sorted(splits, reverse=True)
    return splits[0][1] if splits else -1


def find_lines(page, vert_overlap=0.3):
    lines = []

    for word in page.words:
        overlap = [(find_overlap(ln, word), ln) for ln in lines]
        overlap = sorted(overlap, key=lambda o: -o[0])

        if overlap and overlap[0][0] > vert_overlap:
            line = overlap[0][1]
            line.words.append(word)
        else:
            line = Line()
            line.words.append(word)
            lines.append(line)

    lines = sorted(lines, key=lambda ln: ln.top)
    return lines


def find_overlap(line, word, eps=1):
    """Find the vertical overlap between a line and the word bounding box.

    This is a fraction of the smallest height of the line & word bounding box.
    """
    last = line.words[-1]  # If self.boxes is empty then we have a bigger problem
    min_height = min(last.y_max - last.y_min, word.y_max - word.y_min)
    y_min = max(last.y_min, word.y_min)
    y_max = min(last.y_max, word.y_max)
    inter = max(0, y_max - y_min)
    return inter / (min_height + eps)


def read_html(in_html, min_y, max_y):
    pages = []

    with open(in_html) as in_html:
        doc = in_html.read()

    soup = BeautifulSoup(doc, features="lxml")

    for no, page_elem in enumerate(soup.findAll("page"), 1):
        width = float(page_elem.attrs["width"])
        height = float(page_elem.attrs["height"])
        page = Page(no, width, height)
        pages.append(page)
        bottom = page.height - max_y

        words = []
        for word_elem in page_elem.findAll("word"):
            x_min = round(float(word_elem["xmin"]))
            y_min = round(float(word_elem["ymin"]))
            x_max = round(float(word_elem["xmax"]))
            y_max = round(float(word_elem["ymax"]))
            if y_max >= min_y and y_min <= bottom:
                words.append(Word(x_min, y_min, x_max, y_max, word_elem.text))

        page.words = sorted(words, key=lambda w: w.x_min)

    return pages


def parse_args():
    description = """Convert an XHTML file with word bounding boxes to text."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--in-xhtml",
        type=Path,
        required=True,
        metavar="PATH",
        help="""The XHTML file with the bounding boxes.""",
    )

    arg_parser.add_argument(
        "--out-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the text to this file.""",
    )

    arg_parser.add_argument(
        "--gap-radius",
        type=int,
        default=10,
        help="""Consider a gap to be in the center if it is within this distance of
            the true center of the page. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--gap-min",
        type=int,
        default=12,
        help="""Break a line into 2 columns if the gap between words is near the
            center and the gap is at least this big. Set this to zero if there are
            never 2 columns of text. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--min-y",
        type=int,
        default=75,
        help="""Remove words that are above this distance from the top of the page.
            (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--max-y",
        type=int,
        default=0,
        help="""Remove words that are below this distance from the bottom of the page.
            (default: %(default)s)""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
