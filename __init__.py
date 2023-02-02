from IDRConverter.scheduler import scheduleTask
from IDRConverter.flaskcode import startBackend
from IDRConverter.databasecode import createDatabase

createDatabase()
scheduleTask()
startBackend()