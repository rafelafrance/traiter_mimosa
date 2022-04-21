"""Test the part linker matcher."""
import unittest

from tests.setup import test


class TestPartLinker(unittest.TestCase):
    def test_part_linker_01(self):
        self.assertEqual(
            test("""pinnules up to 31 pairs on pinna-rachis,"""),
            [
                {"part": "pinnule", "trait": "part", "start": 0, "end": 8},
                {
                    "low": 31,
                    "trait": "count",
                    "start": 15,
                    "end": 23,
                    "count_group": "pairs",
                    "part": "pinnule",
                },
                {"part": "pinna-rachis", "trait": "part", "start": 27, "end": 39},
            ],
        )
