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
                    "part": "nectary",
                    "trait": "part",
                    "start": 40,
                    "end": 47,
                    "location": "petiolar",
                    "taxon": "ser. Glanduliferae",
                },
                {
                    "shape": "ovate",
                    "trait": "shape",
                    "start": 52,
                    "end": 57,
                    "location": "petiolar",
                    "part": "anther",
                    "taxon": "ser. Glanduliferae",
                },
                {
                    "part": "anther",
                    "trait": "part",
                    "start": 58,
                    "end": 65,
                    "location": "petiolar",
                    "taxon": "ser. Glanduliferae",
                },
            ],
        )
