#!/usr/bin/python

import operatorek, rysownik, os

# sensitivity = os.argv[1]

otwieracz = operatorek.Operator()
zapisywacz = rysownik.Rysownik()
nazwa_katalogu = input("Podaj nazwe katalogu w ktorym znajduja sie probki:\n")
print("=============================================")
while(nazwa_katalogu == ""):
    nazwa_katalogu = input("Podaj nazwe katalogu w ktorym znajduja sie probki:\n")
    print("=============================================")
if(nazwa_katalogu != ""):
    piki = otwieracz.otworzPliki('./'+str(nazwa_katalogu)+'/')
    zapis = otwieracz.scalPiki(piki)
    zapisywacz.saveData(zapis, nazwa_katalogu)
