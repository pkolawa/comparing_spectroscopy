#!/usr/bin/python
###Klasa sluzaca do operacji na plikach
###

import os, csv, math

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
        pikiScaloneHead = ['Pomiar']
        for pik in pikis:
            pikiScaloneHead.append(pik+(' - abs'))
            pikiScaloneHead.append(pik+(' - delta'))
            pikiScaloneHead.append(pik + (' - proc'))
            pikiScaloneHead.append(' | ')
        pikiScalone.append(pikiScaloneHead)


        maxtab = []
        mintab = []
        mn, mx = 0,0
        mnpos, mxpos = 0,0
        isLookingForMax = False
        isLookingForMin = False
        hasStartedPeak = False


        lookformax = True

        for i in range(timeStart, pikStop, timeDelta):
            pikScalonyTemp = [i]
            # print(i)
            for pik in pikis:
                #Rozpoczecie piku na podstawie danych
                if hasStartedPeak == False:
                    if math.fabs(pikis[pik][i]['proc']) != 100.0 and math.fabs(pikis[pik][i]['proc']) != 200.0 and math.fabs(pikis[pik][i]['proc']) != 0.0:
                        hasStartedPeak = True

                #Dodanie kolumny z danymi odnosnie absorbancji
                if(i < len(pikis[pik])):
                    pikScalonyTemp.append(str(pikis[pik][i]['abs']).replace(".",","))
                else:
                    pikScalonyTemp.append("-")

                #Dodanie kolumny ze zmiana wzgledem poprzedniego pomiaru (delta)
                #Sprawdzenie czy jest jeszcze w tym przedziale czasowym rekord i jezeli jest to przyporzadkowanie danych i rozpoznanie ekstremow funkcji
                if (i < len(pikis[pik])):
                    pikScalonyTemp.append(str(pikis[pik][i]['delta']).replace(".",","))
                    #Sprawdzenie, czy jezeli szukamy minimum nastepuje trend wzrostowy
                    if isLookingForMin == True and pikis[pik][i]['delta'] < 0:
                        mintab.append({'peakPos':i,'peakValue':pikis[pik][i]['abs']})
                    #Zamiana na szukanie maksimum, bo nastepuje trend wzrostowy
                    if hasStartedPeak == True and pikis[pik][i]['delta'] > 0:
                        isLookingForMax = True
                        isLookingForMin = False
                    #sprawdzenie, czy jezeli szukamy minimum, nastepuje trend malejacy
                    if isLookingForMax == True and pikis[pik][i]['delta'] < 0:
                        maxtab.append({'peakPos':i,'peakValue':pikis[pik][i]['abs']})
                    #Zamiana na szukanie minimum, gdyz nastepuje trend malejacy
                    if hasStartedPeak == True and pikis[pik][i]['delta'] < 0:
                        isLookingForMax = False
                        isLookingForMin = True
                #Nie pokazujemy nic, poniewaz w tym pomiarze nie ma juz rekordow
                else:
                    pikScalonyTemp.append("-")

                #Dodanie kolumny ze zmiana podana w procentach
                if (i < len(pikis[pik])):
                    pikScalonyTemp.append(str(pikis[pik][i]['proc']).replace(".",","))
                else:
                    pikScalonyTemp.append("-")

                #Rozdzielenie kolumn
                pikScalonyTemp.append('|')

            pikiScalone.append(pikScalonyTemp)
        #Pokazanie listy ekstremow (minimum)
        print(mintab)
        #Pokazanie listy ekstremow (maksimum)
        print(maxtab)
        
        return pikiScalone