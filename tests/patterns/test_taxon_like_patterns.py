import unittest

from tests.setup import test


class TestTaxonLike(unittest.TestCase):
    def test_taxon_like_01(self):
        self.assertEqual(
            test("""it seems closer to the nearly sympatric M. sensitiva."""),
            [
                {
                    "level": "species",
                    "taxon_like": "M. sensitiva",
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
                    "taxon_like": "M. sensitiva",
                    "trait": "taxon_like",
                    "start": 6,
                    "end": 29,
                    "relation": "similar",
                }
            ],
        )

    def test_taxon_like_03(self):
        self.assertEqual(
            test("""It resembles M. sensitiva in amplitude"""),
            [
                {
                    "level": "species",
                    "taxon_like": "M. sensitiva",
                    "trait": "taxon_like",
                    "start": 3,
                    "end": 25,
                    "relation": "resembles",
                }
            ],
        )

    def test_taxon_like_04(self):
        self.assertEqual(
            test("""sympatric pair of M. sensitiva Harms ex Glaziou"""),
            [
                {
                    "level": "species",
                    "authority": "Harms",
                    "taxon_like": "M. sensitiva",
                    "trait": "taxon_like",
                    "start": 0,
                    "end": 36,
                    "relation": "sympatric",
                }
            ],
        )

    def test_taxon_05(self):
        self.assertEqual(
            test("""vicinis M. sensitiva et M. pachyphloia"""),
            [
                {
                    "level": "species",
                    "taxon_like": ["M. sensitiva", "M. pachyphloia"],
                    "trait": "taxon_like",
                    "start": 0,
                    "end": 38,
                    "relation": "vicinis",
                }
            ],
        )
