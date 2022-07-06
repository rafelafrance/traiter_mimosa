import unittest

from tests.setup import test


class TestPartLocation(unittest.TestCase):
    def test_part_location_01(self):
        self.assertEqual(
            test("stipules 3-8 mm, semiamplexicaul, adnate to petiole for 1-2 mm"),
            [
                {"leaf_part": "stipule", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "length_low": 3.0,
                    "length_high": 8.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 9,
                    "end": 15,
                    "leaf_part": "stipule",
                },
                {
                    "shape": "semiamplexicaul",
                    "trait": "shape",
                    "start": 17,
                    "end": 32,
                    "leaf_part": "stipule",
                },
                {
                    "joined": "adnate",
                    "length_low": 1.0,
                    "length_high": 2.0,
                    "length_units": "mm",
                    "trait": "part_as_loc",
                    "start": 34,
                    "end": 62,
                    "leaf_part": "stipule",
                },
            ],
        )

    def test_part_location_02(self):
        self.assertEqual(
            test("leaves completely embracing stem but not connate"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {
                    "part_as_loc": "embracing stem",
                    "trait": "part_as_loc",
                    "start": 18,
                    "end": 32,
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_part_location_03(self):
        self.assertEqual(
            test("stipules shortly ciliate at margin"),
            [
                {"leaf_part": "stipule", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "leaf_margin": "ciliate",
                    "trait": "leaf_margin",
                    "start": 17,
                    "end": 24,
                    "leaf_part": "stipule",
                },
                {
                    "subpart_as_loc": "at margin",
                    "trait": "subpart_as_loc",
                    "start": 25,
                    "end": 34,
                    "leaf_part": "stipule",
                },
            ],
        )
