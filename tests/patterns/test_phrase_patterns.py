"""Test matching literal phrases."""
# pylint: disable=missing-function-docstring
import unittest

from tests.setup import test


class TestPhrase(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_phrase_01(self):
        self.assertEqual(
            test("Pistillate flowers usually sessile; hypogynous"),
            [
                {
                    "sex": "pistillate",
                    "trait": "sex",
                    "start": 0,
                    "end": 10,
                    "part": "flower",
                },
                {
                    "part": "flower",
                    "trait": "part",
                    "start": 11,
                    "end": 18,
                    "sex": "pistillate",
                },
                {
                    "shape": "sessile",
                    "trait": "shape",
                    "start": 27,
                    "end": 34,
                    "part": "flower",
                },
                {
                    "floral_location": "superior",
                    "trait": "floral_location",
                    "start": 36,
                    "end": 46,
                },
            ],
        )

    def test_phrase_02(self):
        self.assertEqual(
            test("Petals glabrous, deciduous;"),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 6},
                {"duration": "deciduous", "trait": "duration", "start": 17, "end": 26},
            ],
        )

    def test_phrase_03(self):
        self.assertEqual(
            test("leaf blade herbaceous."),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 10},
                {
                    "woodiness": "herbaceous",
                    "trait": "woodiness",
                    "start": 11,
                    "end": 21,
                    "part": "leaf",
                },
            ],
        )
