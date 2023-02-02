from scheduler import scheduleTask
from flaskcode import startBackend
from databasecode import createDatabase

createDatabase()
scheduleTask()
startBackend()
