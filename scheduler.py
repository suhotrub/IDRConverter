from IDRConverter.databasecode import writeToDatabase
from IDRConverter.ratescalculator import calculateRates
from apscheduler.schedulers.background import BackgroundScheduler
import sys
import atexit

def gatherDataAndPutToStorage():
	print('scheduling', file=sys.stderr)
	rates = calculateRates()
	writeToDatabase(rates[1])

def scheduleTask():
	print('This is error output', file=sys.stderr)
	print('This is standard output', file=sys.stdout)
	sched = BackgroundScheduler(daemon=True)
	sched.add_job(func=gatherDataAndPutToStorage, trigger="interval", minutes=1)
	sched.start()
	atexit.register(lambda: sched.shutdown())

