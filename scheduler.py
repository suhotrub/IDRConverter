from IDRConverter.databasecode import writeToDatabase
from IDRConverter.ratescalculator import calculateRates
from apscheduler.schedulers.background import BackgroundScheduler
import sys

def gatherDataAndPutToStorage():
	sys.stderr.write("hello.\n")
	rates = calculateRates()
	sys.stderr.write("loaded.\n")
	writeToDatabase(rates[1])
	sys.stderr.write("wrote.\n")

def scheduleTask():
	sched = BackgroundScheduler(daemon=True)
	sched.add_job(gatherDataAndPutToStorage,'interval',minutes=60)
	sched.start()
