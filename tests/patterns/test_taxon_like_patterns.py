import unittest

from tests.setup import test


class TestTaxonLike(unittest.TestCase):
    def test_taxon_like_01(self):
        self.assertEqual(
            test("""it seems closer to the nearly sympatric M. sensitiva."""),
            [
                {
                    "level": "species",
                    "taxon": "M. sensitiva",
                    "trait": "taxon_like",
                    "start": 30,
                    "end": 52,
                    "relation": "sympatric",
                }
            ],
        )

    def test_taxon_like_02(self):
        self.assertEqual(
            test("""it is similar to M. sensitiva."""),
            [
                {
                    "level": "species",
                    "taxon": "M. sensitiva",
                    "trait": "taxon_like",
                    "start": 6,
                    "end": 29,
                    "relation": "similar",
                }
            ],
        )
