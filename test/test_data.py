import unittest
import os
from src.data.data import readCSV, readCSVCanData, readDirCanData
from src.data.parser import dateParser, loxamDateParser
from src.data.processing import processData
import pandas as pd
import pandas.testing as pdt

bentley = pd.DataFrame({
    "Time": ["11:44:59.000000", "11:45:00.000000", "11:45:01.000000", "11:45:01.000000", "11:46:41.000000"],
    "ID": ["DEADBEEF","DEADBEEF","B1337420","B1337420","DEAFFACE"],
    "Machine": ["bentley", "bentley", "bentley", "bentley", "bentley"],
    "Action": ["run", "run", "run", "run", "run"],
    "Source": ["CSU", "CSU", "CSU", "CSU", "CSU"]
})

ferrari = pd.DataFrame({
    "Time": ["11:25:26.643000","11:25:26.643000","11:25:26.646000","11:25:26.647000","11:25:26.652000",],
    "ID": ["C0000E4","1CFF06E4","CF00400","18FF1F00","CFF1700",],
    "Machine": ["ferrari","ferrari","ferrari","ferrari","ferrari"],
    "Action": ["idle","idle","idle","idle","idle"],
    "Source": ["Loxam","Loxam","Loxam","Loxam","Loxam"]
})

lamborghini = pd.DataFrame({
    "Time": ["15:15:58.643918","15:15:58.643918","15:15:58.653772","15:15:58.653772","15:15:58.664227"],
    "ID": ["0DE","0DE","0DE","0DE","0DE"],
    "Machine": ["lamborghini","lamborghini","lamborghini","lamborghini","lamborghini"],
    "Action": ["run","run","run","run","run"],
    "Source": ["Mendeley","Mendeley","Mendeley","Mendeley","Mendeley",]
})

renault = pd.DataFrame({
    "Time": ["14:12:18.813119","14:12:18.813686","14:12:18.814239","14:12:18.814819","14:12:18.818212"],
    "ID": ["cfe5ae6","10ff80e6","18f009e6","18fec4c0","8fe6ee6"],
    "Machine": ["renault","renault","renault","renault","renault"],
    "Action": ["run","run","run","run","run"],
    "Source": ["Renault","Renault","Renault","Renault","Renault"]
})

class testData(unittest.TestCase):
    
    def setUp(self) -> None:
        self.path = os.path.dirname(os.path.abspath(__file__))
    
    def test_readDirCanData(self):
        path = os.path.join(self.path, "./data")
        expected = [bentley, ferrari, lamborghini, renault]
        out = readDirCanData(path, 100)
        for i, o in enumerate(out):
            pdt.assert_frame_equal(expected[i], o)
        
    def test_readCSVCanData(self):
        path = os.path.join(self.path, "./data/Renault/renault run.csv")
        expected = renault
        out = readCSVCanData(path, 10)
        pdt.assert_frame_equal(out, expected)

    def test_readCSV(self):
        path = os.path.join(self.path, "./data/Renault/renault run.csv")
        expected = pd.DataFrame({
            "Time": ["14:12:18.813119","14:12:18.813686","14:12:18.814239","14:12:18.814819","14:12:18.818212"],
            "ID": ["0xcfe5ae6","0x10ff80e6","0x18f009e6","0x18fec4c0","0x8fe6ee6"]
        })
        out = readCSV(path, ";", 10, 1, 0, dateParser, r"\b0x[0-9A-Fa-f]+\b")
        pdt.assert_frame_equal(out, expected)
        
    def test_readCSV_extraTimepos(self):
        path = os.path.join(self.path, "./data/Loxam/ferrari idle.csv")
        expected = pd.DataFrame({
            "Time": ["11:25:26.643000","11:25:26.643000","11:25:26.646000","11:25:26.647000","11:25:26.652000",],
            "ID": ["C0000E4","1CFF06E4","CF00400","18FF1F00","CFF1700",]
        })
        out = readCSV(path, ";", 10, 4, 2, loxamDateParser, r"\b[0-9A-Fa-f]+\b", extraTimepos=1)
        pdt.assert_frame_equal(out, expected)        
        
if __name__ == "__main__":
    unittest.main()
    
