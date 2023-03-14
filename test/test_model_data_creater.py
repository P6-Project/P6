import unittest
import pandas as pd
from src.graphplot import createDataRow, createDataMatrix, createModelData

bentley = pd.DataFrame({
    "Time": ["11:44:59.000000", "11:45:00.000000", "11:45:01.000000", "11:45:01.000000", "11:46:41.000000",
             "11:44:59.000000", "11:45:00.000000", "11:45:01.000000", "11:45:01.000000", "11:46:41.000000"],
    "ID": ["DEADBEEF", "DEADBEEF", "B1337420", "B1337420", "DEAFFACE", "DEADBEAF", "DEADBEEF", "B1237420", "B1337420",
           "DEAFFACE"],
    "Name": ["bentley", "bentley", "bentley", "bentley", "bentley", "bentley", "bentley", "bentley", "bentley",
             "bentley"],
    "Action": ["run", "run", "run", "run", "run", "run", "run", "run", "run", "run"],
    "Source": ["CSU", "CSU", "CSU", "CSU", "CSU", "CSU", "CSU", "CSU", "CSU", "CSU"]
})

ferrari = pd.DataFrame({
    "Time": ["11:25:26.643000", "11:25:26.643000", "11:25:26.646000", "11:25:26.647000", "11:25:26.652000",
             "11:25:26.643000", "11:25:26.643000", "11:25:26.646000", "11:25:26.647000", "11:25:26.652000"],
    "ID": ["C0000E4", "1CFF06E4", "CF00400", "18FF1F00", "CFF1700", "C0000E4", "1CFF06E4", "CF00400", "18FF1F00",
           "CFF1700"],
    "Name": ["ferrari", "ferrari", "ferrari", "ferrari", "ferrari", "ferrari", "ferrari", "ferrari", "ferrari",
             "ferrari"],
    "Action": ["idle", "idle", "idle", "idle", "idle", "idle", "idle", "idle", "idle", "idle"],
    "Source": ["Loxam", "Loxam", "Loxam", "Loxam", "Loxam", "Loxam", "Loxam", "Loxam", "Loxam", "Loxam"]
})

lamborghini = pd.DataFrame({
    "Time": ["15:15:58.643918", "15:15:58.643918", "15:15:58.653772", "15:15:58.653772", "15:15:58.664227",
             "15:15:58.643918", "15:15:58.643918", "15:15:58.653772", "15:15:58.653772", "15:15:58.664227"],
    "ID": ["0DE", "0DE", "0DE", "0DE", "0DE", "0DE", "0DE", "0DE", "0DE", "0DE"],
    "Name": ["lamborghini", "lamborghini", "lamborghini", "lamborghini", "lamborghini", "lamborghini", "lamborghini",
             "lamborghini", "lamborghini", "lamborghini"],
    "Action": ["run", "run", "run", "run", "run", "run", "run", "run", "run", "run"],
    "Source": ["Mendeley", "Mendeley", "Mendeley", "Mendeley", "Mendeley", "Mendeley", "Mendeley", "Mendeley",
               "Mendeley", "Mendeley"]
})

renault = pd.DataFrame({
    "Time": ["14:12:18.813119", "14:12:18.813686", "14:12:18.814239", "14:12:18.814819", "14:12:18.818212",
             "14:12:18.813119", "14:12:18.813686", "14:12:18.814239", "14:12:18.814819", "14:12:18.818212"],
    "ID": ["cfe5ae6", "10ff80e6", "18f009e6", "18fec4c0", "8fe6ee6", "fe24fde", "18f009e6", "18fec4c0", "8fe6ee6",
           "fe24fde"],
    "Name": ["renault", "renault", "renault", "renault", "renault", "renault", "renault", "renault", "renault",
             "renault"],
    "Action": ["run", "run", "run", "run", "run", "run", "run", "run", "run", "run"],
    "Source": ["Renault", "Renault", "Renault", "Renault", "Renault", "Renault", "Renault", "Renault", "Renault",
               "Renault"]
})


class ModelDataCreaterTester(unittest.TestCase):

    def test_createDataRow(self):
        out = createDataRow(renault, "18fec4c0", 2, 10 / 2)
        self.assertEqual(out, [0, 1, 0, 1, 0])
        out = createDataRow(renault, "1234", 1, 10)
        self.assertEqual(out, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        out = createDataRow(renault, "18fec4c0", 10, 1)
        self.assertEqual(out, [1])

    def test_createDataMatrix(self):
        out = createDataMatrix(renault, ["cfe5ae6", "10ff80e6", "18f009e6", "18fec4c0", "8fe6ee6", "fe24fde"], 2)
        self.assertEqual(out, [[1, 0, 0, 0, 0],
                               [1, 0, 0, 0, 0],
                               [0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0],
                               [0, 0, 1, 0, 1],
                               [0, 0, 1, 0, 1]])

    def test_createModelData(self):
        bentley_matrix = [[1, 1], [1, 1], [1, 1], [0, 1], [0, 1], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                          [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        ferrari_matrix = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [0, 0],
                          [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        lamborghini_matrix = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [1, 1],
                              [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        renault_matrix = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                          [1, 0], [1, 0], [1, 1], [1, 1], [1, 1], [0, 1]]

        target = [1, 2, 3, 4]

        modelData = [bentley_matrix, ferrari_matrix, lamborghini_matrix, renault_matrix]
        outModelData, outTarget = createModelData(
            pd.concat([bentley, ferrari, lamborghini, renault], ignore_index=True, sort=False), 5, 10)
        self.assertEqual(outTarget, target)
        self.assertEqual(outModelData, modelData)
