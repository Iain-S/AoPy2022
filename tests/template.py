import unittest
from src.THE_DAY. import one, two


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/dayTHE_DAY.txt") as f:
            content = [line.rstrip() for line in f]

        expected = -1
        actual = one(content)
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/dayTHE_DAY.txt") as f:
            content = [line.rstrip() for line in f]

        expected = -1
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
