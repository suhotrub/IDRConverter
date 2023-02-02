from IDRConverter.databasecode import writeToDatabase
from IDRConverter.ratescalculator import calculateRates
from apscheduler.schedulers.background import BackgroundScheduler
import sys

sys.stdout = open('output.logs', 'w')

def gatherDataAndPutToStorage():
	print("hello.")
	rates = calculateRates()
	print("loaded.")
	writeToDatabase(rates[1])
	print("wrote.")

def scheduleTask():
	print("hithere.")
	sched = BackgroundScheduler(daemon=True)
	sched.add_job(gatherDataAndPutToStorage,'interval',minutes=60)
	sched.start()
