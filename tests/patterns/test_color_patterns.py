"""Test the plant color matcher."""
import unittest

from tests.setup import test


class TestColor(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_color_01(self):
        self.assertEqual(
            test(
                """hypanthium green or greenish yellow,
                usually not purple-spotted, rarely purple-spotted distally.
            """
            ),
            [
                {"part": "hypanthium", "trait": "part", "start": 0, "end": 10},
                {
                    "color": "green",
                    "trait": "color",
                    "part": "hypanthium",
                    "start": 11,
                    "end": 16,
                },
                {
                    "color": "green-yellow",
                    "trait": "color",
                    "part": "hypanthium",
                    "start": 20,
                    "end": 35,
                },
                {
                    "color": "purple-spotted",
                    "trait": "color",
                    "part": "hypanthium",
                    "missing": True,
                    "start": 45,
                    "end": 63,
                },
                {
                    "color": "purple-spotted",
                    "trait": "color",
                    "part": "hypanthium",
                    "missing": True,
                    "start": 65,
                    "end": 86,
                },
            ],
        )

    def test_color_02(self):
        self.assertEqual(
            test("hypanthium straw-colored to sulphur-yellow or golden-yellow."),
            [
                {"part": "hypanthium", "trait": "part", "start": 0, "end": 10},
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "hypanthium",
                    "start": 11,
                    "end": 24,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "hypanthium",
                    "start": 28,
                    "end": 42,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "hypanthium",
                    "start": 46,
                    "end": 59,
                },
            ],
        )

    def test_color_03(self):
        self.assertEqual(
            test("sepals erect, green- or red-tipped."),
            [
                {"part": "sepal", "trait": "part", "start": 0, "end": 6},
                {
                    "color": "green",
                    "trait": "color",
                    "part": "sepal",
                    "start": 14,
                    "end": 20,
                },
                {
                    "color": "red-tipped",
                    "trait": "color",
                    "part": "sepal",
                    "start": 24,
                    "end": 34,
                },
            ],
        )

    def test_color_04(self):
        self.assertEqual(
            test("petals white, cream, or pale green [orange to yellow]."),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 6},
                {
                    "color": "white",
                    "trait": "color",
                    "part": "petal",
                    "start": 7,
                    "end": 12,
                },
                {
                    "color": "white",
                    "trait": "color",
                    "part": "petal",
                    "start": 14,
                    "end": 19,
                },
                {
                    "color": "green",
                    "trait": "color",
                    "part": "petal",
                    "start": 24,
                    "end": 34,
                },
                {
                    "color": "orange",
                    "trait": "color",
                    "part": "petal",
                    "start": 36,
                    "end": 42,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "petal",
                    "start": 46,
                    "end": 52,
                },
            ],
        )

    def test_color_05(self):
        """It handles pattern notations within colors."""
        self.maxDiff = None
        self.assertEqual(
            test(
                """
                petals distinct, white to cream, greenish yellow,
                maturing yellowish or pale brown, commonly mottled or with
                light green or white longitudinal stripes.
                """
            ),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 6},
                {
                    "color": "white",
                    "trait": "color",
                    "part": "petal",
                    "start": 17,
                    "end": 22,
                },
                {
                    "color": "white",
                    "trait": "color",
                    "part": "petal",
                    "start": 26,
                    "end": 31,
                },
                {
                    "color": "green-yellow",
                    "trait": "color",
                    "part": "petal",
                    "start": 33,
                    "end": 48,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "petal",
                    "start": 59,
                    "end": 68,
                },
                {
                    "color": "brown",
                    "trait": "color",
                    "part": "petal",
                    "start": 72,
                    "end": 82,
                },
                {
                    "color": "green",
                    "trait": "color",
                    "part": "petal",
                    "start": 109,
                    "end": 120,
                },
                {
                    "color": "white-longitudinal-stripes",
                    "trait": "color",
                    "part": "petal",
                    "start": 124,
                    "end": 150,
                },
            ],
        )

    def test_color_06(self):
        self.assertEqual(
            test(
                """
                Petals distinct, white to cream, greenish white,
                or yellowish green, or yellowish, usually green-throated
                and faintly green-lined.
                """
            ),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 6},
                {
                    "color": "white",
                    "trait": "color",
                    "part": "petal",
                    "start": 17,
                    "end": 22,
                },
                {
                    "color": "white",
                    "trait": "color",
                    "part": "petal",
                    "start": 26,
                    "end": 31,
                },
                {
                    "color": "green-white",
                    "trait": "color",
                    "part": "petal",
                    "start": 33,
                    "end": 47,
                },
                {
                    "color": "yellow-green",
                    "trait": "color",
                    "part": "petal",
                    "start": 52,
                    "end": 67,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "petal",
                    "start": 72,
                    "end": 81,
                },
                {
                    "color": "green-throated",
                    "trait": "color",
                    "part": "petal",
                    "start": 91,
                    "end": 105,
                },
                {
                    "color": "green-lined",
                    "trait": "color",
                    "part": "petal",
                    "start": 110,
                    "end": 129,
                },
            ],
        )

    def test_color_07(self):
        self.assertEqual(
            test("calyx yellow"),
            [
                {"part": "calyx", "trait": "part", "start": 0, "end": 5},
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "calyx",
                    "start": 6,
                    "end": 12,
                },
            ],
        )

    def test_color_08(self):
        self.assertEqual(
            test("corolla yellow"),
            [
                {"part": "corolla", "trait": "part", "start": 0, "end": 7},
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "corolla",
                    "start": 8,
                    "end": 14,
                },
            ],
        )

    def test_color_09(self):
        self.assertEqual(
            test("flower yellow"),
            [
                {"part": "flower", "trait": "part", "start": 0, "end": 6},
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "flower",
                    "start": 7,
                    "end": 13,
                },
            ],
        )

    def test_color_10(self):
        self.assertEqual(
            test("hypanthium yellow"),
            [
                {"part": "hypanthium", "trait": "part", "start": 0, "end": 10},
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "hypanthium",
                    "start": 11,
                    "end": 17,
                },
            ],
        )

    def test_color_11(self):
        self.assertEqual(
            test("petal pale sulfur-yellow."),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 5},
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "petal",
                    "start": 6,
                    "end": 24,
                },
            ],
        )

    def test_color_12(self):
        self.assertEqual(
            test("sepal yellow"),
            [
                {"part": "sepal", "trait": "part", "start": 0, "end": 5},
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "sepal",
                    "start": 6,
                    "end": 12,
                },
            ],
        )

    def test_color_13(self):
        self.assertEqual(
            test("Leaves acaulescent or nearly so, with white hairs."),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 6},
                {
                    "habit": "acaulescent",
                    "trait": "habit",
                    "part": "leaf",
                    "start": 7,
                    "end": 18,
                },
                {
                    "color": "white",
                    "trait": "color",
                    "part": "leaf",
                    "subpart": "hair",
                    "start": 38,
                    "end": 43,
                },
                {
                    "subpart": "hair",
                    "part": "leaf",
                    "trait": "subpart",
                    "start": 44,
                    "end": 49,
                },
            ],
        )

    def test_color_14(self):
        self.assertEqual(
            test("leaflets surfaces rather densely spotted with minute blackish dots"),
            [
                {"part": "leaflet", "trait": "part", "start": 0, "end": 8},
                {
                    "subpart": "surface",
                    "part": "leaflet",
                    "trait": "subpart",
                    "start": 9,
                    "end": 17,
                },
                {
                    "color": "black-dots",
                    "trait": "color",
                    "part": "leaflet",
                    "subpart": "surface",
                    "start": 53,
                    "end": 66,
                },
            ],
        )

    def test_color_15(self):
        self.assertEqual(
            test("Petals purplish in life, whitish yel-lowish when dry;"),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 6},
                {
                    "color": "purple",
                    "trait": "color",
                    "part": "petal",
                    "start": 7,
                    "end": 15,
                },
                {
                    "color": "white-yellow",
                    "trait": "color",
                    "part": "petal",
                    "start": 25,
                    "end": 43,
                },
            ],
        )

    def test_color_16(self):
        self.assertEqual(
            test("Petals red or golden yellowish"),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 6},
                {
                    "color": "red",
                    "trait": "color",
                    "part": "petal",
                    "start": 7,
                    "end": 10,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "part": "petal",
                    "start": 14,
                    "end": 30,
                },
            ],
        )

    def test_color_17(self):
        self.assertEqual(
            test("twigs: young growth green or reddish-tinged."),
            [
                {"part": "twig", "trait": "part", "start": 0, "end": 5},
                {
                    "color": "green",
                    "trait": "color",
                    "part": "twig",
                    "start": 20,
                    "end": 25,
                },
                {
                    "color": "red-tinged",
                    "trait": "color",
                    "part": "twig",
                    "start": 29,
                    "end": 43,
                },
            ],
        )


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
