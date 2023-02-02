from IDRConverter.scheduler import scheduleTask
from IDRConverter.flaskcode import startBackend
from IDRConverter.databasecode import createDatabase

if __name__ == "__main__":
	createDatabase()
	scheduleTask()
	startBackend()
