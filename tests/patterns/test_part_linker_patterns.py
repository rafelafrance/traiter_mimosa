import unittest

from tests.setup import test


class TestPartLinker(unittest.TestCase):
    def test_part_linker_01(self):
        self.assertEqual(
            test("""pinnules up to 31 pairs,"""),
            [
                {"leaf_part": "pinnule", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "low": 31,
                    "trait": "count",
                    "start": 15,
                    "end": 23,
                    "count_group": "pairs",
                    "leaf_part": "pinnule",
                },
            ],
        )

    def test_part_linker_02(self):
        self.assertEqual(
            test(
                """trees closely resembling another thing in habit,
                attaining 2-4 m in height with trunk"""
            ),
            [
                {"part": "tree", "trait": "part", "start": 0, "end": 5},
                {
                    "height_low": 2.0,
                    "height_high": 4.0,
                    "height_units": "m",
                    "trait": "size",
                    "start": 59,
                    "end": 74,
                    "part": "tree",
                },
                {"part": "trunk", "trait": "part", "start": 80, "end": 85},
            ],
        )
