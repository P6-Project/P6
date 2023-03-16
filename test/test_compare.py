import unittest
import os
import pandas as pd


from src.compareJ1939 import compareKnownIDs


knownsIds : pd.DataFrame = pd.DataFrame({"ID_HEX":["ffa12", "ac12f"]})
machines : pd.DataFrame = pd.DataFrame({
    "ID":["ffa12", "ac12f", "ffa12", "ac12f", "ffa16", "ac14f", "ffb12", "ac12c"],
    "Machine":["Machine1", "Machine1", "Machine1", "Machine1", "Machine1", "Machine1", "Machine1", "Machine1"],
})

class testCompare(unittest.TestCase):
    
    def test_compareKnownIDs(self):
        out = compareKnownIDs(knownsIds, machines)
        self.assertEqual(out, ["Machine1"])