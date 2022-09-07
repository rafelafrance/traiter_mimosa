"""Image transforms performed on images before OCR."""
# type: ignore
import functools
import re
from typing import Callable
from typing import Literal
from typing import Union

import numpy as np
import pytesseract
from numpy import typing as npt
from PIL import Image
from PIL.Image import Image as ImageType
from pytesseract.pytesseract import TesseractError
from scipy import ndimage
from scipy.ndimage import interpolation as interp
from skimage import exposure as ex
from skimage import filters
from skimage import morphology as morph

ImageOrNumpy = Union[ImageType, npt.ArrayLike]
Transformation = Callable[[ImageOrNumpy], ImageOrNumpy]


def compose(*functions: Transformation) -> Transformation:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


def image_to_array(image: ImageType) -> np.ndarray:
    image = image.convert("L")
    return np.asarray(image)  # noqa


def array_to_image(image: npt.ArrayLike) -> ImageType:
    if hasattr(image, "dtype") and image.dtype == "float64":
        mode: Union[None, Literal] = "L" if len(image.shape) < 3 else "RGB"
        return Image.fromarray(image * 255.0, mode)
    if hasattr(image, "dtype") and image.dtype == "bool":
        image = (image * 255).astype("uint8")
        mode = "L" if len(image.shape) < 3 else "RGB"
        return Image.fromarray(image, mode)
    return Image.fromarray(image, "L")


def scale(
    image: npt.ArrayLike,
    factor: float = 2.0,
    min_dim: int = 512,
    mode: str = "constant",
) -> npt.ArrayLike:
    if image.shape[0] < min_dim or image.shape[1] < min_dim:
        image = ndimage.zoom(image, factor, mode=mode)
    return image


def blur(image: npt.ArrayLike, sigma: float = 1.0) -> npt.ArrayLike:
    image = ndimage.gaussian_filter(image, sigma)
    return image


def orient(
    image: npt.ArrayLike,
    conf_low: float = 15.0,
    conf_high: float = 100.0,
) -> npt.ArrayLike:
    try:
        osd = pytesseract.image_to_osd(image)
    except TesseractError:
        return image

    angle = 0
    if match := re.search(r"Rotate: (\d+)", osd):
        angle = int(match.group(1))

    conf = 0.0
    if match := re.search(r"Orientation confidence: ([\d.]+)", osd):
        conf = float(match.group(1))

    if angle != 0 and conf_low <= conf <= conf_high:
        image = ndimage.rotate(image, angle, mode="nearest")

    return image


def deskew(image: npt.ArrayLike, horiz_angles: npt.ArrayLike = None) -> npt.ArrayLike:
    """Find the skew of the image.

    This method is looking for sharp breaks between the characters and spaces.
    It will work best with binary images.
    """
    if not horiz_angles:
        horiz_angles = np.array([0.0, 0.5, -0.5, 1.0, -1.0, 1.5, -1.5, 2.0, -2.0])

    array = np.array(image).astype(np.int8)
    scores = []
    for angle in horiz_angles:
        rotated = interp.rotate(array, angle, reshape=False, order=0)
        proj = np.sum(rotated, axis=1)
        score = np.sum((proj[1:] - proj[:-1]) ** 2)
        scores.append(score)
    best = max(scores)
    angle = horiz_angles[scores.index(best)]

    if angle != 0.0:
        image = ndimage.rotate(image, angle, mode="nearest")

    return image


def rank_mean(image: npt.ArrayLike, footprint=None) -> npt.ArrayLike:
    image = filters.rank.mean(image, footprint)
    return image


def rank_median(image: npt.ArrayLike) -> npt.ArrayLike:
    image = filters.rank.median(image)
    return image


def rank_modal(image: npt.ArrayLike) -> npt.ArrayLike:
    image = filters.rank.median(image)
    return image


def equalize_hist(image: npt.ArrayLike) -> npt.ArrayLike:
    image = ex.equalize_hist(image)
    image = (image * 255).astype(np.int8)
    return image


def exposure(image: npt.ArrayLike, gamma: float = 2.0) -> npt.ArrayLike:
    image = ex.adjust_gamma(image, gamma=gamma)
    image = ex.rescale_intensity(image)
    return image


def binarize_sauvola(
    image: npt.ArrayLike,
    window_size: int = 11,
    k: float = 0.032,
) -> npt.ArrayLike:
    threshold = filters.threshold_sauvola(image, window_size=window_size, k=k)
    image = image > threshold
    return image


def remove_small_holes(
    image: npt.ArrayLike,
    area_threshold: int = 64,
    connectivity: int = 1,
) -> npt.ArrayLike:
    image = morph.remove_small_holes(
        image, area_threshold=area_threshold, connectivity=connectivity
    )
    return image


def binary_opening(image: npt.ArrayLike) -> npt.ArrayLike:
    image = morph.binary_opening(image)
    return image


# =============================================================================
# Canned scripts for transforming images

# If you plan to use an ensemble every ensemble pipeline must include the same
# affine transforms that modify the geometry of the image [Scale, Orient, Deskew].
# Else wise, it becomes almost impossible to align bounding boxes of each
# ensemble member. For instance, in the PIPELINES below you must use the same:
# Scale(), Orient(), Deskew() in every ensemble member because they change the
# geometry but you could exclude Blur() because it does not.

TRANSFORM_START: Transformation = compose(
    image_to_array,
    functools.partial(blur, sigma=0.5),
    functools.partial(scale, mode="nearest"),
    orient,
    deskew,
)

TRANSFORM_PIPELINES: dict[str, Transformation] = {
    "deskew": compose(TRANSFORM_START, array_to_image),
    "binarize": compose(TRANSFORM_START, binarize_sauvola, array_to_image),
    "denoise": compose(
        TRANSFORM_START,
        binarize_sauvola,
        remove_small_holes,
        binary_opening,
        array_to_image,
    ),
}


def transform_label(pipeline: str, image: ImageType) -> ImageType:
    """Transform the image to improve OCR results."""
    return TRANSFORM_PIPELINES[pipeline](image)
