import pyodbc
sqlServerName = "VR-PC123"

cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=' + sqlServerName + ';'
                      'Database=master;'
                      'Trusted_Connection=yes;', autocommit=True)

print("Connected to Sql Server " + sqlServerName)

cursor = cnxn.cursor()

dbName = "VRX_pacificnational"

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

