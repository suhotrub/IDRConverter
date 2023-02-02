from IDRConverter.databasecode import writeToDatabase
from IDRConverter.ratescalculator import calculateRates
from apscheduler.schedulers.background import BackgroundScheduler
import sys
import atexit
import os

def gatherDataAndPutToStorage():
	rates = calculateRates()
	writeToDatabase(rates[1])

def scheduleTask():
	sched = BackgroundScheduler(daemon=True)
	sched.add_job(func=gatherDataAndPutToStorage, trigger="interval", minutes=1)
	sched.start()
	atexit.register(lambda: sched.shutdown())

