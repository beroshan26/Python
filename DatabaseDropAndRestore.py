import pyodbc
import time
import sys

cmdArgs = list(sys.argv)

sqlServerName = cmdArgs[1]

cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=' + sqlServerName + ';'
                      'Database=master;'
                      'Trusted_Connection=yes;', autocommit=True)

print("Connected to Sql Server " + sqlServerName)

cursor = cnxn.cursor()

dbName = cmdArgs[2]

backUpFileName = cmdArgs[3]

tempFolder = cmdArgs[4]

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

print("Waiting few seconds after restore...")

time.sleep(20)

print("Resetting details in database")
			 
sqlResetCommand = ("Use [" + dbName + "] ;\
                    Update [dbo].EmailSettings Set IsEnabled = 0 where IsEnabled = 1; \
                    update [dbo].[PaymentSettings] Set IsWestpactPaymentEnabled = 0 where IsWestpactPaymentEnabled = 1;\
		    update [dbo].[Job] set statuscode=1 where statuscode <>1;\
                    update UserProfile set passwordhash = 'T5AWdhbHQ919vnvcw+ncHMEDVESx5vOjRKwMtGaMAt4=',\
                    PasswordSalt = 'eSUOUqiAY/sW0jpSsAzwSw==', ChangePassword = 0, LastPasswordChangeDate = SYSDATETIME();")
			 
cursor.execute(sqlResetCommand)

print("Reset complete")

cursor.commit()
cnxn.commit()