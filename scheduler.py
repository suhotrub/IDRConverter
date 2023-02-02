from IDRConverter.databasecode import writeToDatabase
from IDRConverter.ratescalculator import calculateRates
from apscheduler.schedulers.background import BackgroundScheduler
import sys
import atexit
import os

def gatherDataAndPutToStorage():
	print('scheduling', file=sys.stderr)
	rates = calculateRates()
	print('loaded', file=sys.stderr)
	writeToDatabase(rates[1])
	print('wrote', file=sys.stderr)
	print(rates[1], file=sys.stderr)

def scheduleTask():
	if  os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
		print('This is error output', file=sys.stderr)
		print('This is standard output', file=sys.stdout)
		sched = BackgroundScheduler(daemon=True)
		sched.add_job(func=gatherDataAndPutToStorage, trigger="interval", minutes=1)
		sched.start()
		atexit.register(lambda: sched.shutdown())

