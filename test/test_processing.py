import unittest

import pandas as pd
import pandas.testing as pdt

from src.data.processing import limit, milis, normalizeDF, normalizeTime


class testProcessing(unittest.TestCase):
    def test_normalizeDF(self):
        input = pd.DataFrame(
            {
                "Time": [
                    "13:37:00.100000",
                    "13:37:00.300000",
                    "13:37:00.400000",
                    "13:37:00.700000",
                    "13:37:00.900000",
                    "13:37:01.200000",
                ],
                "ID": [1, 2, 3, 4, 5, 6],
            }
        )
        expected = pd.DataFrame(
            {"Time": [0, 200, 300, 0, 200, 500], "ID": [1, 2, 3, 4, 5, 6]}
        )

        out = normalizeDF(input, 3)

        pdt.assert_frame_equal(out, expected)

    def test_limit(self):
        input = pd.DataFrame(
            {
                "Time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            }
        )
        excepted = pd.DataFrame(
            {"Time": [1, 2, 3, 4, 5, 6, 7, 8], "ID": [1, 2, 3, 4, 5, 6, 7, 8]}
        )
        out = limit(input, 4)

        pdt.assert_frame_equal(out, excepted)

    def test_normalizeTime(self):
        input = [
            "13:37:00.100000",
            "13:37:00.300000",
            "13:37:00.400000",
            "13:37:00.700000",
            "13:37:00.900000",
            "13:37:01.200000",
        ]
        expected = [0, 200, 300, 0, 200, 500]
        out = normalizeTime(input, 3)
        self.assertEqual(out, expected)

    def test_milis(self):
        out = milis("13:37:00.420000")
        self.assertEqual(out, 49020420)


if __name__ == "__main__":
    unittest.main()
