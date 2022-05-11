"""Test the taxon linker matcher."""
import unittest

from tests.setup import test


class TestTaxonLinker(unittest.TestCase):
    """Test the taxon trait linker."""

    def test_taxon_linker_01(self):
        self.assertEqual(
            test(
                """ser. Glanduliferae, in which a petiolar nectary and ovate anthers,"""
            ),
            [
                {
                    "level": "series",
                    "taxon": "ser. Glanduliferae",
                    "trait": "taxon",
                    "start": 0,
                    "end": 18,
                },
                {
                    "flower_part": "nectary",
                    "trait": "flower_part",
                    "start": 40,
                    "end": 47,
                    "taxon": "ser. Glanduliferae",
                    "location": "petiolar",
                },
                {
                    "shape": "ovate",
                    "trait": "shape",
                    "start": 52,
                    "end": 57,
                    "male_flower_part": "anther",
                    "taxon": "ser. Glanduliferae",
                },
                {
                    "male_flower_part": "anther",
                    "trait": "male_flower_part",
                    "start": 58,
                    "end": 65,
                    "taxon": "ser. Glanduliferae",
                    "location": "petiolar",
                },
            ],
        )
