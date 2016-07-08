#!/usr/bin/python
### Klasa sluzaca do rysowania pikow na jednym grafie
###

import csv

class Rysownik:

	def __init__(self):
		pass

	def saveData(self, insertedData):
		with open('samples/output.csv', 'w', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			for datas in insertedData:
				spamwriter.writerow(datas)