#!/usr/bin/python

import operatorek, rysownik, os

# sensitivity = os.argv[1]

otwieracz = operatorek.Operator()
zapisywacz = rysownik.Rysownik()
piki = otwieracz.otworzPliki('samples/')
zapis = otwieracz.scalPiki(piki)
zapisywacz.saveData(zapis)