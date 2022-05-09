"""Test the plant margin shape matcher."""
# pylint: disable=missing-function-docstring
import unittest

from tests.setup import test


class TestMargin(unittest.TestCase):
    """Test the plant margin shape trait parser."""

    def test_margin_01(self):
        self.assertEqual(
            test("margin shallowly undulate-crenate"),
            [
                {"subpart": "margin", "trait": "subpart", "start": 0, "end": 6},
                {
                    "leaf_margin": "undulate-crenate",
                    "trait": "leaf_margin",
                    "subpart": "margin",
                    "start": 7,
                    "end": 33,
                },
            ],
        )

    def test_margin_02(self):
        self.maxDiff = None
        self.assertEqual(
            test("margins ciliate, apex acute to long-acuminate,"),
            [
                {"subpart": "margin", "trait": "subpart", "start": 0, "end": 7},
                {
                    "leaf_margin": "ciliate",
                    "trait": "leaf_margin",
                    "subpart": "margin",
                    "start": 8,
                    "end": 15,
                },
                {"subpart": "apex", "trait": "subpart", "start": 17, "end": 21},
                {
                    "leaf_shape": "acute",
                    "trait": "leaf_shape",
                    "subpart": "apex",
                    "start": 22,
                    "end": 27,
                },
                {
                    "shape": "acuminate",
                    "trait": "shape",
                    "subpart": "apex",
                    "start": 31,
                    "end": 45,
                },
            ],
        )

    def test_margin_03(self):
        self.assertEqual(
            test("reniform, undulate-margined"),
            [
                {"leaf_shape": "reniform", "trait": "leaf_shape", "start": 0, "end": 8},
                {
                    "leaf_margin": "undulate",
                    "trait": "leaf_margin",
                    "start": 10,
                    "end": 27,
                },
            ],
        )

    def test_margin_04(self):
        self.assertEqual(
            test("margins thickened-corrugated"),
            [
                {"subpart": "margin", "trait": "subpart", "start": 0, "end": 7},
                {
                    "leaf_margin": "corrugated",
                    "trait": "leaf_margin",
                    "subpart": "margin",
                    "start": 8,
                    "end": 28,
                },
            ],
        )

    def test_margin_05(self):
        self.assertEqual(
            test(
                """
                margins coarsely toothed or remotely sinuate-dentate
                to serrate,"""
            ),
            [
                {"subpart": "margin", "trait": "subpart", "start": 0, "end": 7},
                {
                    "leaf_margin": "toothed",
                    "trait": "leaf_margin",
                    "subpart": "margin",
                    "start": 8,
                    "end": 24,
                },
                {
                    "leaf_margin": "sinuate-dentate",
                    "trait": "leaf_margin",
                    "subpart": "margin",
                    "start": 28,
                    "end": 52,
                },
                {
                    "leaf_margin": "serrate",
                    "trait": "leaf_margin",
                    "subpart": "margin",
                    "start": 56,
                    "end": 63,
                },
            ],
        )
