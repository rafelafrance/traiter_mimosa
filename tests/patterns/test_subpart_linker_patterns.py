import unittest

from tests.setup import test


class TestSubpartLinker(unittest.TestCase):
    def test_subpart_linker_01(self):
        self.assertEqual(
            test("""limbs (1-) 2-4 (-5) pairs;"""),
            [
                {"subpart": "limb", "trait": "subpart", "start": 0, "end": 5},
                {
                    "min": 1,
                    "low": 2,
                    "high": 4,
                    "max": 5,
                    "trait": "count",
                    "start": 6,
                    "end": 25,
                    "count_group": "pairs",
                    "subpart": "limb",
                },
            ],
        )
