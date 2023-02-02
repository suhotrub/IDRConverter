import csv
import time
import os
path = "database.csv"    

def createDatabase():
    if os.path.isfile(path):
        return

    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Stock price","Tinkoff CNY","Korona GEL USDT", "Korona GEL Credo USDT", "Tinkoff USDT", "Unistream GEL USDT", "TBC USD IDR"])


def writeToDatabase(table):
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            round(time.time()*1000),
            table["Stock price"],
            table["Tinkoff CNY"],
            table["Korona GEL USDT"],
            table["Korona GEL Credo USDT"],
            table["Tinkoff USDT"],
            table["Unistream GEL USDT"],
            table["TBC USD IDR"],
         ])