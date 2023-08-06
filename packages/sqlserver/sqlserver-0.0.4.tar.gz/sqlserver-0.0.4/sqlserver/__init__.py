# ADGSTUDIOS 2021
# PYTHON SQL SERVER MODULE
# 2021/06/10 16h09
# REV 0.0.2

import pyodbc


class sqlserver():
    def __init__(self, ip, port, Database, UserName, Password):
        try:
            if port == '':
                self.ip = ip
            else:
                self.ip = ip+','+port

            self.database = Database
            if UserName == "" and Password == "":
                self.logindetails = "Trusted_Connection=yes;"
            else:
                self.logindetails = "UID="+UserName+";PWD="+Password+";"
        except Exception as e:
            print("use strings for all input")

    def ExecuteQuery(self, Query):
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                  'Server='+self.ip+';'
                                  'Database='+self.database+';'
                                  '%s' % (self.logindetails))
            cursor = conn.cursor()
            cursor.execute(Query)
            cursor.commit()
            print("Query Executed")
        except Exception as e:
            print(e)

    def fields(self, cur):
        results = {}
        column = 0
        for d in cur.description:
            results[d[0]] = column
            column = column + 1

        return results

    def GetRecordsOfColumn(self, SelectQuery, ColumnName):
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                  'Server='+self.ip+';'
                                  'Database='+self.database+';'
                                  '%s' % (self.logindetails))
            cursor = conn.cursor()
            cursor.execute(SelectQuery)
            field_map = self.fields(cursor)
            values = []
            for row in cursor:
                values.append(row[field_map[ColumnName]])
            return values
        except Exception as e:
            print(e)

    def RunStoredProcedure(self, StoredProcedureName):
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                  'Server='+self.ip+';'
                                  'Database='+self.database+';'
                                  '%s' % (self.logindetails))
            cursor = conn.cursor()
            cursor.execute("exec "+StoredProcedureName)
            print("Stored Procedure Executed : "+StoredProcedureName)
        except Exception as e:
            print(e)
