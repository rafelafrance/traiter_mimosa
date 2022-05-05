"""Test matching literal phrases."""
# pylint: disable=missing-function-docstring
import unittest

from tests.setup import test


class TestPartLocation(unittest.TestCase):
    """Test the plant part parser."""

    def test_part_location_01(self):
        self.assertEqual(
            test("stipules 3-8 mm, semiamplexicaul, adnate to petiole for 1-2 mm"),
            [
                {"part": "stipule", "trait": "part", "start": 0, "end": 8},
                {
                    "length_low": 3.0,
                    "length_high": 8.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 9,
                    "end": 15,
                    "part": "stipule",
                },
                {
                    "length_low": 1.0,
                    "length_high": 2.0,
                    "length_units": "mm",
                    "trait": "part_as_loc",
                    "start": 41,
                    "end": 62,
                    "part": "stipule",
                },
            ],
        )

    def test_part_location_02(self):
        self.assertEqual(
            test("leaves completely embracing stem but not connate"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 6},
                {
                    "part_as_loc": "embracing stem",
                    "trait": "part_as_loc",
                    "start": 18,
                    "end": 32,
                    "part": "leaf",
                },
                {
                    "shape": "not connate",
                    "trait": "shape",
                    "start": 37,
                    "end": 48,
                    "part": "leaf",
                },
            ],
        )

    def test_part_location_03(self):
        self.assertEqual(
            test("stipules shortly ciliate at margin"),
            [
                {"part": "stipule", "trait": "part", "start": 0, "end": 8},
                {
                    "margin_shape": "ciliate",
                    "trait": "margin_shape",
                    "start": 17,
                    "end": 24,
                    "part": "stipule",
                },
                {
                    "subpart_as_loc": "at margin",
                    "trait": "subpart_as_loc",
                    "start": 25,
                    "end": 34,
                    "part": "stipule",
                },
            ],
        )
