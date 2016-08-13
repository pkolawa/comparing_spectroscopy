#!/usr/bin/python
###Klasa sluzaca do operacji na plikach
###

import os, csv


class Operator():
	piki = {}

	def __init__(self):
		pass

	# def rozpakujZIP(self):

	def otworzPliki(self, directory):
		for infile in os.listdir(directory):
			infileDir = directory + infile
			with open(infileDir, 'r') as csvfile:
				pik = []
				spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
				i = 0
				for row in spamreader:
					if(row[0] == "s" or row[0] == "Created as New Dataset"):
						continue
					sekunda = int(float(row[0].replace(",",".")))
					abs = float(row[1].replace(",","."))
					delta_perc = 0.00000
					if (i == 0):
						delta = 0.0
					else:
						j = i - 1
						abs_wstecz = pik[j]['abs']
						delta = round(abs - pik[j]['abs'], 5)
						if (pik[j]['abs'] != 0):
							delta_perc =  round((delta / abs_wstecz) * 100, 5)
					#Dodaje tablice z wynikiem w danej sekundzie (tozsamej z indexem tablicy)
					pik.append({'czas':sekunda, 'abs':abs, 'delta':delta, 'proc':delta_perc})
					i = i + 1
				self.piki[infile] = pik

		return self.piki

		# for pomiar in self.piki:
		# 	print(pomiar['1'])

	def scalPiki(self, pikis):
		#sprawdzenie czy w kazdej serii jest identyczna liczba pomiarow
		pikiCount = 0
		notSameCount = False
		for pik in pikis:
			timeStart = pikis[pik][0]['czas']
			timeDelta = pikis[pik][1]['czas'] - timeStart
			if(len(pik) and pikiCount != 0):
				pikiCount = len(pikis[pik])
				notSameCount = True
			elif(pikiCount == 0):
				pikiCount = len(pikis[pik])
			pikStop = pikiCount - 1
			timeStop = pikis[pik][pikStop]['czas']

		# print(timeStart)
		# print(timeStop)
		# print(timeDelta)
		# print(pikStop)

		pikiScalone = []
		pikiScaloneHead = ['czas']
		for pik in pikis:
			pikiScaloneHead.append(pik+(' - abs'))
		pikiScaloneHead.append(' | ')
		for pik in pikis:
			pikiScaloneHead.append(pik+(' - delta'))
		pikiScaloneHead.append(' | ')
		for pik in pikis:
			pikiScaloneHead.append(pik + (' - proc'))
		pikiScalone.append(pikiScaloneHead)

		for i in range(timeStart, pikStop, timeDelta):
			pikScalonyTemp = [i]
			# print(i)
			for pik in pikis:
				if(i < len(pikis[pik])):
					pikScalonyTemp.append(str(pikis[pik][i]['abs']).replace(".",","))
				else:
					pikScalonyTemp.append(0)

			pikScalonyTemp.append(' | ')

			for pik in pikis:
				if (i < len(pikis[pik])):
					pikScalonyTemp.append(str(pikis[pik][i]['delta']).replace(".",","))
				else:
					pikScalonyTemp.append(0)

			pikScalonyTemp.append(' | ')

			for pik in pikis:
				if (i < len(pikis[pik])):
					pikScalonyTemp.append(str(pikis[pik][i]['proc']).replace(".",","))
				else:
					pikScalonyTemp.append(0)

			pikiScalone.append(pikScalonyTemp)

		return pikiScalone