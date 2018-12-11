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

sqlFileList = "restore filelistonly  FROM  DISK = " + backUpFileName

cursor.execute(sqlFileList)

print("Obtained Filelist from " + backUpFileName)

rows = list(cursor)

mdfLogicalFileName = rows[0][0]

ldfLogicalFileName = rows[1][0]


sqlcommand = "USE [master]; \
               RESTORE DATABASE " + dbName + " FROM  DISK = " + backUpFileName + " \
               WITH REPLACE,\
               MOVE '" + mdfLogicalFileName + "' TO '" + tempFolder + mdfLogicalFileName + ".mdf',"" \
               MOVE '" + ldfLogicalFileName + "' TO '" + tempFolder + ldfLogicalFileName + ".ldf';"    

print(sqlcommand)
cursor.execute(sqlcommand)

print("Sql Command Executed")

cursor.commit()

cnxn.commit()


print("Database "  + dbName + " Restored")
