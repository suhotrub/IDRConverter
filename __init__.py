from IDRConverter.flaskcode import startBackend, app
from IDRConverter.databasecode import createDatabase

createDatabase()

if __name__ == "__main__":
	startBackend()
