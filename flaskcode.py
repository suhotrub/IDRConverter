from flask import Flask, render_template
from IDRConverter.ratescalculator import calculateRates
from prettytable import PrettyTable

app = Flask(__name__, static_url_path='',static_folder='static',template_folder='template')

@app.route("/")
def main():
	rates = calculateRates()

	variablesTable = PrettyTable()
	variablesTable.field_names = ["Key", "Value"]
	for key, value in rates[0].items():
		variablesTable.add_row([key, value])

	resultTable = PrettyTable()
	resultTable.field_names = ["Route", "1k IDR in RUB"]
	for key, value in rates[1].items():
		resultTable.add_row([key, value])
	resultTable.sortby = "1k IDR in RUB"

	return variablesTable.get_html_string() + "<br><br>" + resultTable.get_html_string() + "<br>" + render_template("template.html")

def startBackend():
	app.run(use_reloader=False)
