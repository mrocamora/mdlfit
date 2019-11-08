# encoding: utf-8
import numpy
import math
import matplotlib.pyplot as plt  # para graficar
from auxiliares import escribir

#Largo de descripcion de corpus en 4/4, usando MDL-BIC

#importo funciones para los parametros
from funciones_parametros import parametrosM1, parametrosM2, parametrosM344, parametrosM444, parametrosM544, parametrosM644, parametrosM744, parametrosMtotal44

#Largo de descripcion de corpus en 4/4, usando MDL-BIC

#Largos de descripcion segun los distintos modelos
def L1(lista, d):
	pM1 = parametrosM1(lista)[2]
	n = len(lista[0:-1])
	entropia = -n*(pM1*numpy.log2(pM1) + (1-pM1)*numpy.log2(1-pM1))
	return (entropia + 2*numpy.log2(d))*8/n

def L2(lista, d):
	n = len(lista[0:-1])
	pM2 = parametrosM2(lista, 8)
	validas = pM2 !=0
	pM1 = parametrosM1(lista)[2]
	entropia = -n*pM1*numpy.dot(pM2[validas],numpy.log2(pM2[validas]))
	return (entropia + len(pM2)*numpy.log2(d))*8/n

def L3(lista,d):
	pM3 = parametrosM344(lista)
	n = len(lista[0:-1])
	enes = [n/8, n/8, n/4, n/2]
	entropia = -sum(numpy.array(enes)*(numpy.array(pM3)*numpy.array(numpy.log2(pM3)) + (1 -numpy.array(pM3))*numpy.array(numpy.log2(1 - numpy.array(pM3))))) 
	return (entropia + (len(pM3) +1)*numpy.log2(d))*8/n

def L4(lista, d):
	pM4 = parametrosM444(lista)
	n = len(lista[0:-1])
	entropia = -(n/8)*(numpy.dot(pM4,numpy.log2(pM4)) + numpy.dot(1 - numpy.array(pM4),numpy.log2(1 - numpy.array(pM4))) )
	return (entropia + (len(pM4) +1)*numpy.log2(d))*8/n

def L5(lista, d):
	pM5 = parametrosM544(lista)
	n = len(lista[0:-1])
	tetaaux = numpy.array(pM5[0])
	validas = (tetaaux!= 0)*(tetaaux!=1) 
	nijs = numpy.array(pM5[1])[validas]
	beats = numpy.array(pM5[2])[validas]
	entropia = - numpy.dot(nijs, numpy.log2(tetaaux[validas])) - numpy.dot(beats -nijs,  numpy.log2(1 - tetaaux[validas]))
 	return (entropia + (len(tetaaux) +1)*numpy.log2(d))*8/n

def L6(lista, d):
	pM6 = parametrosM644(lista)
	pM4 = parametrosM444(lista)
	n = len(lista[0:-1])
	entropia = - numpy.dot(n*numpy.array(pM4)/8, [numpy.dot(v[v>0],(numpy.log2(v[v>0]))) for v in pM6])
 	return (entropia + 13*numpy.log2(d))*8/n

def L7(lista,d):
	pM7 = parametrosM744(lista)
	n = len(lista[0:-1])
	tetaaux = numpy.array(pM7[0])
	validas = (tetaaux!= 0)*(tetaaux!=1) 
	nijs = numpy.array(pM7[1])[validas]
	beats = numpy.array(pM7[2])[validas]
	entropia = -numpy.dot(nijs, numpy.log2(tetaaux[validas])) - numpy.dot(beats -nijs, numpy.log2(1 - tetaaux[validas]))
 	return (entropia + (len(tetaaux) +1)*numpy.log2(d))*8/n

def LMtotal(lista,d):
	pMtotal = parametrosMtotal44(lista)
	n = len(lista[0:-1])
	tetaaux = numpy.array(pMtotal[0])
	validas = (tetaaux!= 0)*(tetaaux!=1) 
	nijs = numpy.array(pMtotal[1])[validas]
	beats = numpy.array(pMtotal[2])[validas]
	entropia = -numpy.dot(nijs, numpy.log2(tetaaux[validas])) - numpy.dot(beats -nijs, numpy.log2(1 - tetaaux[validas]))
 	return (entropia + (len(tetaaux) +1)*numpy.log2(d))*8/n



#### Para los distintos corpus y d = sqrt(N) calculo los largos
listavalores = []

for archivo in ['golpesEssenFolksong44.txt', 'golpesairdsAirs44.txt', 'golpesoneills185044.txt', 'golpesSatorre_cancionero44.txt']:
	datos = open(archivo, "r")
	datosaux = datos.readlines()
	listagolpes = []
	for sec in datosaux[0:-1]: #Terminan con una linea que tiene solo un salto
		listagolpes.append([int(x.strip()) for x in sec.split(' ')])
	tiragrande = []
	for tira in listagolpes:
		tiragrande.extend(tira[0:-1]) #saque los unos del final
	tiragrande.append(1) #agrego un ultimo 1
	tiragrande = tiragrande[:801] #TEST PARA VERSION REDUCIDA
	d = numpy.sqrt(len(tiragrande))
	listavalores.append([L1(tiragrande, d), L2(tiragrande, d), L3(tiragrande, d), L4(tiragrande, d), L5(tiragrande, d),L6(tiragrande, d), L7(tiragrande, d) , LMtotal(tiragrande, d)])

escribir(listavalores, 'listavalores_crudeMDL44REDUCIDA')

listaslargos = []

des = [pow(2, de) for de in range(3,12)]
for archivo in ['golpesEssenFolksong44.txt', 'golpesairdsAirs44.txt', 'golpesoneills185044.txt', 'golpesSatorre_cancionero44.txt']:  
	datos = open(archivo, "r")
	datosaux = datos.readlines()
	listagolpes = []
	for sec in datosaux[0:-1]: #Terminan con una linea que tiene solo un salto
		listagolpes.append([int(x.strip()) for x in sec.split(' ')])
	tiragrande = []
	for tira in listagolpes:
		tiragrande.extend(tira[0:-1]) #saque los unos del final
	tiragrande.append(1) #agrego un ultimo 1
	listaslargos.append([ [L1(tiragrande, de) for de in des], [L2(tiragrande, de) for de in des], [L3(tiragrande, de) for de in des], [L4(tiragrande, de) for de in des], [L5(tiragrande, de) for de in des], [L6(tiragrande, de) for de in des], [L7(tiragrande, de) for de in des]  , [LMtotal(tiragrande,de) for de in des] ])
