import sqlite3


def createDatabase(table: list, database: str):
    con = sqlite3.connect(database)
    cur = con.cursor()

    cur.execute("""CREATE TABLE Machines (
    Id INTEGER PRIMARY KEY,
    Time varchar(255) NOT NULL,
    CanID VARCHAR(255) NOT NULL,
    Machine VARCHAR(255) NOT NULL,
    MachineAction VARCHAR(255) NOT NULL,
    Source VARCHAR(255) NOT NULL
);""")
    insert = createDBInsert(table)
    cur.execute(insert)
    con.commit()

    

def createDBInsert(table: list):
    insert = "INSERT INTO Machines (Time, CanID, Machine, MachineAction, Source) VALUES {values};"
    value = '("{time}", "{id}", "{machine}", "{machineAction}", "{source}"){end}'
    values = ""
    maxLen = len(table[0])
    for i in range(maxLen):
        last = i == maxLen - 1
        values += value.format(
            time=table[0][i], id=table[1][i], machine=table[2][i], 
            machineAction=table[3][i], source=table[4][i], end=("" if last else ",")
            )
    return insert.format(values=values)