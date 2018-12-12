import pyodbc
sqlServerName = "VR-PC123"

cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=' + sqlServerName + ';'
                      'Database=master;'
                      'Trusted_Connection=yes;', autocommit=True)

print("Connected to Sql Server " + sqlServerName)

cursor = cnxn.cursor()

dbName = "VRX_pacificnational"

backUpFileName = "'F:\TestBed\destination\VRX_Pacificnational_13112018.bak'"

tempFolder = ("F:\\temp\\")

sqlDropCommand = ("IF (EXISTS (SELECT name FROM master.dbo.sysdatabases WHERE name = '" + dbName + "'))\n" +
                    "Begin \n" +
                    "Drop Database " + dbName + "\n"
                    "End")
             
print("Dropping database " + dbName)
			 
cursor.execute(sqlDropCommand)

print("Dropped database " + dbName)

sqlFileListCmd = "restore filelistonly  FROM  DISK = " + backUpFileName

cursor.execute(sqlFileListCmd)

print("Obtained Filelist from " + backUpFileName)

rows = list(cursor)

mdfLogicalFileName = rows[0][0]

ldfLogicalFileName = rows[1][0]


sqlRestoreCommand = "USE [master]; \
               RESTORE DATABASE " + dbName + " FROM  DISK = " + backUpFileName + " \
               WITH REPLACE,\
               MOVE '" + mdfLogicalFileName + "' TO '" + tempFolder + mdfLogicalFileName + ".mdf',"" \
               MOVE '" + ldfLogicalFileName + "' TO '" + tempFolder + ldfLogicalFileName + ".ldf';"    

print("Restoring database " + dbName)

#print(sqlRestoreCommand)
cursor.execute(sqlRestoreCommand)

print("Database "  + dbName + " Restored")

cursor.commit()

cnxn.commit()

