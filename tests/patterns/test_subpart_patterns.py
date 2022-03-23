"""Test matching literal phrases."""
# pylint: disable=missing-function-docstring
import unittest

from tests.setup import test


class TestSubpart(unittest.TestCase):
    """Test the plant subpart parser."""

    def test_subpart_01(self):
        self.assertEqual(
            test("terminal lobe ovate-trullate,"),
            [
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 9,
                    "end": 13,
                    "location": "terminal",
                },
                {
                    "shape": "ovate-trullate",
                    "trait": "shape",
                    "start": 14,
                    "end": 28,
                    "subpart": "lobe",
                },
            ],
        )
