import pyodbc as sql
from datetime import datetime

class SqlHelper:
    def __init__(self, db_name='TrashPanda') -> None:
        self.sql_connection = sql.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE='+db_name)
        self.cursor = self.sql_connection.cursor()
    
    def Insert(self, values, table_name='PriceInfo'):
        tsql = f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?);"

        with self.cursor.execute(tsql, values[0], values[1], values[2], values[3], values[4], values[5], values[6]):
            print ('Successfully Inserted!')

    def Update(self):
        #Draft
        tsql = "UPDATE Employees SET Location = ? WHERE Name = ?"

        with self.cursor.execute(tsql,'Sweden','Nikita'):
            print ('Successfully Updated!')

    def Delete(self):
        #Draft
        tsql = "DELETE FROM Employees WHERE Name = ?"

        with self.cursor.execute(tsql,'Jared'):
            print ('Successfully Deleted!')

    def Read(self):
        #Draft
        tsql = "SELECT Name, Location FROM Employees;"

        with self.cursor.execute(tsql):
            row = self.cursor.fetchone()

            while row:
                print (str(row[0]) + " " + str(row[1]))
                row = self.cursor.fetchone()

sql_helper = SqlHelper()

sql_helper.Insert(['2019.05.28 07:33:00', 10040.1, 10040.8, 10040.1, 10040.7, 3, 'Step Index'])


