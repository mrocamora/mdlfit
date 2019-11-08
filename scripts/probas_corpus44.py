# encoding: utf-8

import copy
import numpy
from auxiliares import escribir
import os
from collections import Counter

#Manipulo las tiras de 1s y 0s exportadas por corpusObras44. Algunas funciones sirven para otras tiras con otras subdivisiones también.

#primero levanto los datos, los pego como una única tira (sacando los 1s que se agregaron al final)

from menuTemperleyMDL import archivo

#archivo = 'golpesSatorre_cancionero44.txt' #elegir

datos = open(archivo, "r")
datosaux = datos.readlines()

listagolpes = []
for sec in datosaux[0:-1]: #Terminan con una linea que tiene solo un salto
	listagolpes.append([int(x.strip()) for x in sec.split(' ')])


tiragrande = []
for tira in listagolpes:
	tiragrande.extend(tira[0:-1]) #saque los unos del final

tiragrande.append(1) #agrego un ultimo 1

from funciones_parametros import parametrosM1, parametrosM2
from funciones_parametros import parametrosM344 as parametrosM3
from funciones_parametros import parametrosM444 as parametrosM4 
from funciones_parametros import parametrosM544 as parametrosM5
from funciones_parametros import parametrosM644 as parametrosM6
from funciones_parametros import parametrosM744 as parametrosM7
from funciones_parametros import parametrosMtotal44 as parametrosMtotal


#Modelo 1: hallo la proporción de 1s total. 
#Aplico las funciones
pM1 = parametrosM1(tiragrande)[2] #proba
pM2 = parametrosM2(tiragrande, 8) #vector de probas, Temperley usa 16 (2 compases) en vez de 8
pM3 = parametrosM3(tiragrande)
pM4 = parametrosM4(tiragrande) #vector de 8
pM5 = parametrosM5(tiragrande)
pM6 = parametrosM6(tiragrande)
pM7 = parametrosM7(tiragrande)
pMtotal = parametrosMtotal(tiragrande)

#exporto parametros. Elijo nombre de archivo segun nombre de archivo con golpes

#archivoparametros = 'parametros_' +  archivo[6:] #cambio 'golpes' por 'parametros_'
#archi = open(archivoparametros, 'wb')
#archi.write(str(pM1) + '\n' + str(pM2) + '\n' + str(pM3) + '\n' + str(pM4) + '\n' + str(pM5) + '\n' + str(pM6) + '\n' + str(pM7) + '\n' + str(pMtotal))
#archi.close()
