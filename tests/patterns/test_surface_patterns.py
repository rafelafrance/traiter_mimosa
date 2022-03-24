"""Test the plant surface patterns."""
import unittest

from tests.setup import test


class TestSurface(unittest.TestCase):
    """Test the plant surface patterns."""

    def test_surface_01(self):
        self.assertEqual(
            test("""glabrous flowers"""),
            [
                {
                    "surface": "glabrous",
                    "trait": "surface",
                    "start": 0,
                    "end": 8,
                    "part": "flower",
                },
                {"part": "flower", "trait": "part", "start": 9, "end": 16},
            ],
        )
