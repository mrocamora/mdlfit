# encoding: utf-8

from music21 import *
import copy
import numpy
from auxiliares import escribir
import os

###CÓDIGO PARA EXTRAER LOS GOLPES DEL CORPUS SATORRE (u otros)

###Como las obras se encuentran ya filtradas, el código asume que las obras están completamente en 4/4
### En el caso de las que tienen ataque fuera de corchea, simplemente ignoro los ataques fuera de grilla (ver corpus: no hay sincopas cortas. Parece tener sentido hacerlo)
### Escribo el código de modo que sirva también para cualquier posible corpus enteramente en 4/4


nombrecarpeta = 'Satorre_cancionero44'  #modificar si se quiere usar otro corpus
ruta = 'otroscorpus/' + nombrecarpeta + '/'
listaarchivos = [ruta + archi for archi in os.listdir(ruta)] #Rutas de los archivos a abrir
nobras = len(listaarchivos)


listagolpes = nobras*[[]] #Tantas listas vacias como max de obras
bpc = 8 #beats por compas
indice = 0

for archi in listaarchivos:
	obrita = converter.parse(archi).parts[0]
	compases = obrita.getElementsByClass('Measure')
	ncompas = len(compases)
	golpesobrita = (bpc*ncompas +1)*[0] #todos los golpes de la obra, más uno extra al final si corresponde
	for l in range(ncompas): #itero en los compases
		compasactual = compases[l].flat.notes 
		lugaresgolpes = [((x.beat -1)/0.5)  for x in compasactual if ((x.beat -1)/0.5).is_integer()] #los lugares en beat de corchea en que hay ataque
		golpescompas = numpy.array(bpc*[0]); golpesenteros = [int(x) for x in lugaresgolpes] #inicializo compas de ceros
		golpescompas[golpesenteros] = 1 #si el compas es vacio no cambia nada
		golpesobrita[l*bpc:(l+1)*bpc] = golpescompas
	#terminó iteración en los compases
	if golpesobrita[-bpc:] == [0,0,0,0,0,0,0,0]: #termina con un solo golpe en el primer beat. No agrego nada, saco los ultimos 7 ceros por coherencia
		golpesobrita = golpesobrita[:-bpc]
	else:
		golpesobrita[-1] = 1 #el 1 al final de la obra 
	listagolpes[indice] = golpesobrita 
	indice +=1

listagolpes = listagolpes[:indice] #sado las listas vacias correspondientes a obras que no se agregaron


escribir(listagolpes, 'golpes' + nombrecarpeta)

