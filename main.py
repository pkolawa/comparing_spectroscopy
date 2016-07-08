#!/usr/bin/python

import operator, rysownik, os

# sensitivity = os.argv[1]


otwieracz = operator.Operator()
zapisywacz = rysownik.Rysownik()
piki = otwieracz.otworzPliki('samples/')
zapis = otwieracz.scalPiki(piki)
zapisywacz.saveData(zapis)