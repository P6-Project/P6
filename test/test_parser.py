import unittest

from src.data.parser import (
    CSUDateParser,
    CSUIDParser,
    dateParser,
    loxamDateParser,
    renaultIDParser,
)


class testParser(unittest.TestCase):
    def test_CSUDateParser(self):
        out = CSUDateParser("(1337420699.000000)")
        self.assertEqual(out, "11:44:59.000000")

    def test_CSUIDParser(self):
        out = CSUIDParser("DEADBEEF#FFFFFFFFFFFFFFFF")
        self.assertEqual(out, "DEADBEEF")

    def test_loxamDateParser(self):
        out = loxamDateParser("03/03/2023 11:25:26,647,000")
        self.assertEqual(out, "11:25:26.647000")

    def test_dateParser(self):
        out = dateParser("2018-07-26 15:15:58.653772")
        self.assertEqual(out, "15:15:58.653772")

    def test_renaultIDParser(self):
        out = renaultIDParser("0xdeadface")
        self.assertEqual(out, "deadface")


if __name__ == "__main__":
    unittest.main()
