from IDRConverter.flaskcode import app
from IDRConverter.databasecode import createDatabase
import sys
import threading
import time

def start_runner():
	print('Trying to start server', file=sys.stderr)
	def start_loop():
		not_started = True
		while not_started:
			print('In start loop', file=sys.stderr)
			try:
				r = requests.get('http://127.0.0.1:5000/')
				if r.status_code == 200:
					print('Server started, quiting start_loop', file=sys.stderr)
					not_started = False
				print(r.status_code)
			except:
				print('Server not yet started', file=sys.stderr)
			time.sleep(2)

	print('Started runner', file=sys.stderr)
	thread = threading.Thread(target=start_loop)
	thread.start()

createDatabase()
start_runner()