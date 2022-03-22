"""Test the taxon matcher."""
import unittest

from tests.setup import test


class TestTaxon(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_taxon_01(self):
        self.assertEqual(
            test("""M. sensitiva"""),
            [{"species": "M. sensitiva", "trait": "species", "start": 0, "end": 12}],
        )

    def test_taxon_02(self):
        self.assertEqual(
            test("""Mimosa sensitiva"""),
            [
                {
                    "species": "Mimosa sensitiva",
                    "trait": "species",
                    "start": 0,
                    "end": 16,
                }
            ],
        )

    def test_taxon_03(self):
        self.assertEqual(
            test("""M. polycarpa var. spegazzinii"""),
            [
                {
                    "variant": "M. polycarpa var. spegazzinii",
                    "trait": "variant",
                    "start": 0,
                    "end": 29,
                }
            ],
        )
