import unittest

from tests.setup import test


class TestSubpartLinker(unittest.TestCase):
    def test_subpart_linker_01(self):
        self.assertEqual(
            test("""pinnae (1-) 2-4 (-5) pairs;"""),
            [
                {"subpart": "pinnae", "trait": "subpart", "start": 0, "end": 6},
                {
                    "min": 1,
                    "low": 2,
                    "high": 4,
                    "max": 5,
                    "trait": "count",
                    "start": 7,
                    "end": 26,
                    "count_group": "pairs",
                    "subpart": "pinnae",
                },
            ],
        )
