#!/usr/bin/python
###Klasa sluzaca do operacji na plikach
###

import os, csv, math
from matplotlib import pyplot as plt
import numpy as np
import matplotlib

class Operator():
    piki = {}

    def __init__(self):
        pass

    # def rozpakujZIP(self):

    def otworzPliki(self, directory):
        print(os.listdir(directory))
        for infile in os.listdir(directory):
            if infile == ".DS_Store" or infile == "output.csv":
                os.remove(directory + infile)
            else:
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
        pikiScaloneHead = ['Pomiar']
        for pik in pikis:
            pikiScaloneHead.append(pik+(' - abs'))
            pikiScaloneHead.append(pik+(' - delta'))
            pikiScaloneHead.append(pik + (' - proc'))
            pikiScaloneHead.append('====')
        pikiScalone.append(pikiScaloneHead)


        #Szukanie poczatku pierwszego piku
        pikStart = {}
        for pik in pikis:
            pikStart[pik] = 0

        for pik in pikis:
            if pikStart[pik] == 0:
                for i in range(timeStart, pikStop, timeDelta):
                    if 100.0 != pikis[pik][i]['proc'] and 200.0 != pikis[pik][i]['proc'] and 0.0 != pikis[pik][i]['proc'] and 50.0 != pikis[pik][i]['proc'] and -100.0 != pikis[pik][i]['proc'] and -200.0 != pikis[pik][i]['proc'] and -50.0 != pikis[pik][i]['proc']:
                        pikStart[pik] = i
                        break
            else:
                break

        #Usuwanie szumow przed pikiem
        for pik in pikis:
            for i in range(0, pikStart[pik], timeDelta):
                pikis[pik].pop(0)
            pikis[pik].insert(0,{'abs':0.0,'delta':0.0,'proc':0.0})

        #Szukanie najdluzszego pomiaru celem usuniecia ogona wynikajacego z uciecia poczatku
        longestArray = 0
        for pik in pikis:
            if len(pikis[pik]) > longestArray:
                longestArray = len(pikis[pik])

        #Rysowanie wykresu
        colors = ['g','b','r','y','navy','fuchsia','deeppink','turquoise','cyan','dodgerblue','peru','lightsage']
        colorIndex = 0
        for pik in pikis:
            for i in range(timeStart, longestArray, timeDelta):
                if (i < len(pikis[pik])):
                    if i == timeStart:
                        plt.scatter(i, pikis[pik][i]['abs'], 40, c=colors[colorIndex], alpha=0.5, label=pik)
                    else:
                        plt.scatter(i, pikis[pik][i]['abs'], 40, c=colors[colorIndex], alpha=0.5)
            colorIndex += 1
            if colorIndex == 5:
                colorIndex = 0

        #Scalanie piku
        for i in range(timeStart, longestArray, timeDelta):
            pikScalonyTemp = [i]
            for pik in pikis:
                #Dodanie kolumny z danymi odnosnie absorbancji
                if(i < len(pikis[pik])):
                    pikScalonyTemp.append(str(pikis[pik][i]['abs']).replace(".",","))
                else:
                    pikScalonyTemp.append("")

                #Dodanie kolumny ze zmiana wzgledem poprzedniego pomiaru (delta)
                #Sprawdzenie czy jest jeszcze w tym przedziale czasowym rekord i jezeli jest to przyporzadkowanie danych i rozpoznanie ekstremow funkcji
                if (i < len(pikis[pik])):
                    pikScalonyTemp.append(str(pikis[pik][i]['delta']).replace(".",","))
                #Nie pokazujemy nic, poniewaz w tym pomiarze nie ma juz rekordow
                else:
                    pikScalonyTemp.append("")

                #Dodanie kolumny ze zmiana podana w procentach
                if (i < len(pikis[pik])):
                    pikScalonyTemp.append(str(pikis[pik][i]['proc']).replace(".",","))
                else:
                    pikScalonyTemp.append("")

                #Rozdzielenie kolumn
                pikScalonyTemp.append('====')

            pikiScalone.append(pikScalonyTemp)

        #Pytanie o wartosci w danym punkcie
        keepAsking = True
        while keepAsking:
            selectedTime = input("Podaj czas, ktory chcesz sprawdzic \n(aby zakonczyc, nacisnij Q)\n")
            if selectedTime == "Q" or selectedTime == "q":
                keepAsking = False
            else:
                selectedTime = int(selectedTime)
                print("==================================")
                print("Dla pomiaru " + str(selectedTime) + " po znormalizowaniu wartosci wynosza odpowiedni:")
                for pik in pikis:
                    print(pik + ": "+ str(pikis[pik][selectedTime]['abs']))
                print("==================================\n\n")

        plt.xlabel("Czas")
        plt.ylabel("Abs")
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.show()

        return pikiScalone