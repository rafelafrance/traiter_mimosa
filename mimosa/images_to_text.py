#!/usr/bin/env python3
"""Convert images of PDF pages into text via OCR."""
import argparse
import textwrap
from pathlib import Path

import pytesseract
import rich
import skimage
from PIL import Image
from tqdm import tqdm


CHAR_BLACKLIST = "¥€£¢$«»®©™§|"
TESS_LANG = "eng"


def main():
    """Convert the file."""
    args = parse_args()

    page_images_to_text(args)

    msg = " ".join("""You may need to edit this file manually.""".split())
    rich.print(f"\n[bold yellow]{msg}[/bold yellow]\n")


def page_images_to_text(args):
    """Convert images of PDF pages into text via OCR."""
    pages = sorted(args.image_dir.glob("*.jpg"))

    with open(args.out_text, "w") as text_file:
        for page in tqdm(pages):
            image = skimage.io.imread(page)

            is_two_columns = args.columns == 2
            texts = pipeline(image, is_two_columns)
            text_file.writelines(texts)


def pipeline(image, is_two_columns, sigma=11):
    """Convert one page image into text."""
    image = skimage.img_as_float(image)
    gray = skimage.color.rgb2gray(image)

    blurred = skimage.filters.gaussian(gray, sigma=sigma)

    # threshold = filters.threshold_sauvola(blurred, window_size=WINDOW_SIZE, k=K)
    threshold = skimage.filters.threshold_otsu(blurred)
    binary = blurred > threshold

    inverted = skimage.util.invert(binary)
    labeled = skimage.measure.label(inverted)

    regions = get_regions(labeled, is_two_columns)
    regions = sort_regions(image, regions)

    texts = regions_to_text(regions, gray)

    return texts


def regions_to_text(regions, gray, min_words=8):
    """OCR each region of text."""
    tess_config = " ".join(
        [
            f"-l {TESS_LANG}",
            f"-c tessedit_char_blacklist='{CHAR_BLACKLIST}'",
        ]
    )
    texts = []

    for region in regions:
        top, left, bottom, right = get_bbox(region, gray.shape)
        cropped = gray[top:bottom, left:right] * 255.0
        cropped = Image.fromarray(cropped).convert("RGB")
        text = pytesseract.image_to_string(cropped, config=tess_config)
        if len(text.split()) > min_words:
            texts.append(text)

    return texts


def region_key(region, threshold, shape):
    """The sort order of the regions."""
    top, left, bottom, right = get_bbox(region, shape)
    return left // threshold, top, left


def sort_regions(image, regions, pad=50):
    """Order the text regions so the text flows properly."""
    threshold = (image.shape[1] // 2) - pad
    return sorted(regions, key=lambda r: region_key(r, threshold, image.shape))


def get_regions(labeled, is_two_columns):
    """Get regions of text."""
    regions = sorted(
        skimage.measure.regionprops(labeled),
        key=lambda r: r.area,
        reverse=True,
    )
    regions = [r for r in regions if not too_small(r, labeled.shape)]

    big_regions = []
    for region in regions:
        for bigger in big_regions:
            if inside(region, bigger):
                break
        else:
            big_regions.append(region)

    if is_two_columns:
        regions = [r for r in big_regions if not too_wide(r, labeled.shape)]

    return regions


def inside(smaller_region, bigger_region):
    """Remove smaller bounding boxes that overlap with bigger bounding boxes."""
    s_top, s_left, s_bottom, s_right = smaller_region.bbox
    b_top, b_left, b_bottom, b_right = bigger_region.bbox

    top_left = b_top < s_top < b_bottom and b_left < s_left < b_right
    bottom_right = b_top < s_bottom < b_bottom and b_left < s_right < b_right
    top_right = b_top < s_top < b_bottom and b_left < s_right < b_right
    bottom_left = b_top < s_bottom < b_bottom and b_left < s_left < b_right

    return any([top_left, bottom_right, top_right, bottom_left])


def too_wide(region, shape, pad=50):
    """Remove regions that are too wide.

    A method to get rid of headers, footers, and figure captions is to remove text
    that spans too many columns.
    """
    top, left, bottom, right = get_bbox(region, shape)
    width = right - left
    return width > (shape[1] // 2) + pad


def get_bbox(region, shape, border=6):
    """Create a clear border around the text."""
    height, width = shape[:2]
    top, left, bottom, right = region.bbox
    top = max(top - border, 0)
    left = max(left - border, 0)
    bottom = min(bottom + border, height)
    right = min(right + border, width)
    return top, left, bottom, right


def too_small(region, shape, min_height=50, min_width=100):
    """Get rid of headers and footers and other small stray marks."""
    top, left, bottom, right = get_bbox(region, shape)
    width = right - left
    height = bottom - top
    return width < min_width or height < min_height


def parse_args():
    """Process command-line arguments."""
    description = """Convert images of (."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--image-dir",
        type=Path,
        required=True,
        metavar="DIR",
        help="""The directory with the images of the pages.""",
    )

    arg_parser.add_argument(
        "--out-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the text to this file.""",
    )

    arg_parser.add_argument(
        "--columns",
        type=int,
        choices=[1, 2],
        default=2,
        help="""How many columns does the text have. (default: %(default)s)""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
