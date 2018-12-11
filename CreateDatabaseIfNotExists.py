import pyodbc
sqlServerName = "VR-PC123"

cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=' + sqlServerName + ';'
                      'Database=master;'
                      'Trusted_Connection=yes;', autocommit=True)

print("Connected to Sql Server " + sqlServerName)

cursor = cnxn.cursor()

dbName = "VRX_pacificnational"

sqlcommand = ("IF (NOT EXISTS (SELECT name FROM master.dbo.sysdatabases WHERE name = '" + dbName + "'))\n" +
                    "Begin \n" +
                    "Create Database " + dbName + "\n"
                    "End")
             

cursor.execute(sqlcommand)

print("Sql Command Executed")

cursor.commit()

cnxn.commit()


print("Database "  + dbName + " Created or Exists")
