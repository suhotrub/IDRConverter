from IDRConverter.databasecode import writeToDatabase
from IDRConverter.ratescalculator import calculateRates
from apscheduler.schedulers.background import BackgroundScheduler

def gatherDataAndPutToStorage():
	print("loading rates for database")
	rates = calculateRates()
	print("rates loaded, writing to database")
	writeToDatabase(rates[1])
	print("success")

def scheduleTask():
	sched = BackgroundScheduler(daemon=True)
	sched.add_job(gatherDataAndPutToStorage,'interval',minutes=60)
	sched.start()
