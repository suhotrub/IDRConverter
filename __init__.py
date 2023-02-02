from IDRConverter.scheduler import scheduleTask
from IDRConverter.flaskcode import startBackend, app
from IDRConverter.databasecode import createDatabase

createDatabase()
scheduleTask()

if __name__ == "__main__":
	startBackend()
