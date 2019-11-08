# encoding: utf-8

import copy
import numpy
from auxiliares import escribir
import os
from collections import Counter

###funciones para calcular los parametros en general
def parametrosM1(lista): #recibe una lista de unos y ceros
	n1 = sum(lista); n = len(lista)
	return [n1, n, float(n1)/n]

#Modelo 2: hallo todas las probabilidades interataque. Cuenta la cantidad de ceros que hay entre 2 unos.

def parametrosM2(lista, indices): #indices es un número que indica el máx intervalo a considerar. Luego trunco y normalizo
	contador = 0
	dime = lista.count(1) #asi no modifico tamaño de lista
	tiraaux = numpy.array(dime*[1000], dtype = numpy.int32)
	k=0
	for beat in lista:
		if beat == 1:
			tiraaux[k] = contador
			contador = 0; k +=1 #reseteo contador, incremento indice
		contador +=1
	param = range(max(tiraaux))
	cuenta = numpy.bincount(tiraaux)
	naux = len(tiraaux)
	for i in param:
		param[i] = float(cuenta[i+1])/naux  
	param = numpy.array(param[: indices])/sum(param[: indices])
	return param


#funciones especificas para los parametros en 4/4

#Modelo 3: Hallo las probas de ataque de cada nivel (4 niveles)
def parametrosM344(lista):
	beatsnivel4 = lista[0:-1:8] #excluye al ultimo 1
	beatsnivel3 = lista[4::8]
	beatsnivel2 = lista[2::4]
	beatsnivel1 = lista[1::2]
	return [numpy.mean(beatsnivel4), numpy.mean(beatsnivel3), numpy.mean(beatsnivel2), numpy.mean(beatsnivel1)]


#Modelo 4: hallo las probas de ataque de cada posición

def parametrosM444(lista):
	salida = [0,0,0,0,0,0,0,0]
	for k in range(8):
		salida[k] = numpy.mean(lista[k::8])
	return salida

#Modelo 5: hallo las probas de los distintos tipos de anclaje y distintos niveles. En total son 13.

def parametrosM544(lista):#devuelve [[probas], [golpes]]
	p4 = numpy.mean(lista[0:-1:8]) #otra vez la proba de nivel 4
	n = len(lista) -1
	beats1un = 0; beats1pre = 0; beats1post = 0; beats1bi = 0 
	beats2un = 0; beats2pre = 0; beats2post = 0; beats2bi = 0 
	beats3un = 0; beats3pre = 0; beats3post = 0; beats3bi = 0 
	golpes1un = 0; golpes1pre = 0; golpes1post = 0; golpes1bi = 0
	golpes2un = 0; golpes2pre = 0; golpes2post = 0; golpes2bi = 0
	golpes3un = 0; golpes3pre = 0; golpes3post = 0; golpes3bi = 0
	listacontrol = (n/4)*[4] #guardo los indices de nivel 2 que controle
	for i in range(n/8): #obs que uso division entera
		if lista[8*i] == 1: #nivel 3 pre o bi
			if lista[8*(i+1)] == 1: #nivel 3 bi
				beats3bi += 1 
				if lista[8*i +4] == 1:#golpe en nivel 3
					golpes3bi +=1
					beats2bi += 2 #posición 2 y 6, beat bianclado
					if lista[8*i +2] == 1: #posición 1 y 3 bi
						golpes2bi += 1
						beats1bi +=2
						if lista[8*i + 1] == 1:
							golpes1bi +=1
						if lista[8*i + 3] == 1:
							golpes1bi +=1
					else: #posición 1 pre, posición 3 post
						beats1pre +=1; beats1post +=1
						if lista[8*i + 1] == 1:
							golpes1pre +=1
						if lista[8*i + 3] == 1:
							golpes1post +=1
					if lista[8*i + 6] ==1: #posición 5 y 7 bi
						golpes2bi += 1
						beats1bi +=2
						if lista[8*i + 5] == 1:
							golpes1bi +=1
						if lista[8*i + 7] == 1:
							golpes1bi +=1
					else: #posición 5 pre, posición 7 post
						beats1pre +=1; beats1post +=1
						if lista[8*i + 5] == 1:
							golpes1pre +=1
						if lista[8*i + 7] == 1:
							golpes1post +=1
				else: #no golpe en lv 3, beats de posición 2 pre y de posición 6 post
					beats2pre +=1
					beats2post += 1
					if lista[8*i +2] == 1: #posición 1 bi, posición 3 pre
						golpes2pre += 1
						beats1bi +=1; beats1pre +=1
						if lista[8*i + 1] == 1:
							golpes1bi +=1
						if lista[8*i + 3] == 1:
							golpes1pre +=1
					else: #posición 1 pre, posición 3 un
						beats1pre +=1; beats1un +=1
						if lista[8*i + 1] == 1:
							golpes1pre +=1
						if lista[8*i + 3] == 1:
							golpes1un +=1
					if lista[8*i + 6] ==1: #posición 5 post, posición 7 bi
						golpes2post +=1
						beats1bi +=1; beats1post +=1
						if lista[8*i + 5] == 1:
							golpes1post +=1
						if lista[8*i + 7] == 1:
							golpes1bi +=1
					else: #posición 5 un, posición 7 post
						beats1un +=1; beats1post +=1
						if lista[8*i + 5] == 1:
							golpes1un +=1
						if lista[8*i + 7] == 1:
							golpes1post +=1
			else: #nivel 3 pre, posición 6 pre o un, posición 2 pre o bi
				beats3pre += 1
				if lista[8*i +4] == 1: 
					golpes3pre +=1 
					beats2bi +=1 #posición 2 bianclado
					beats2pre += 1 #posición 6 pre
					if lista[8*i +2] ==1: #posición 1 y 3 bi
						golpes2bi+=1
						beats1bi +=2
						if lista[8*i + 1] == 1:
							golpes1bi +=1
						if lista[8*i + 3] == 1:
							golpes1bi +=1
					else: #posición 1 pre, posición 3 post
						beats1pre +=1; beats1post +=1
						if lista[8*i + 1] == 1:
							golpes1pre +=1
						if lista[8*i + 3] == 1:
							golpes1post +=1
					if lista[8*i + 6] ==1: #posición 5 bi, posición 7 pre
						golpes2pre +=1
						beats1bi +=1; beats1pre += 1
						if lista[8*i + 5] == 1:
							golpes1bi +=1
						if lista[8*i + 7] == 1:
							golpes1pre +=1
					else: # posición 5 pre, posición 7 un
						beats1pre +=1; beats1un +=1
						if lista[8*i + 5] == 1:
							golpes1pre +=1
						if lista[8*i + 7] == 1:
							golpes1un +=1
				else: #no golpes en nivel 3. posición 2 pre, posición 6 un
					beats2pre +=1
					beats2un += 1 #posición 6 pre
					if lista[8*i +2] ==1: #posición 1 bi, posición 3 pre
						golpes2pre+=1
						beats1bi +=1; beats1pre += 1
						if lista[8*i + 1] == 1:
							golpes1bi +=1
						if lista[8*i + 3] == 1:
							golpes1pre +=1
					else: #posición 1 pre, posición 3 un
						beats1un +=1; beats1pre += 1
						if lista[8*i + 1] == 1:
							golpes1pre +=1
						if lista[8*i + 3] == 1:
							golpes1un +=1
					if lista[8*i + 6] ==1: #posición 5 post, posición 7 pre
						golpes2un +=1
						beats1post +=1; beats1pre += 1
						if lista[8*i + 5] == 1:
							golpes1post +=1
						if lista[8*i + 7] == 1:
							golpes1pre +=1
					else: #posición 5 un, posición 7 un
						beats1un +=2
						if lista[8*i + 5] == 1:
							golpes1un +=1
						if lista[8*i + 7] == 1:
							golpes1un +=1
		else: # nivel 3 un o post
			if lista[8*(i+1)] == 1: #nivel 3 post
				beats3post += 1
				if lista[8*i +4] == 1: #posición 2 post, posición 6 bi
					golpes3post +=1
					beats2post +=1; beats2bi+= 1
					if lista[8*i +2] == 1: #posición 1 post, posición 3 bi
						golpes2post +=1
						beats1post +=1; beats1bi += 1
						if lista[8*i + 1] == 1:
							golpes1post +=1
						if lista[8*i + 3] == 1:
							golpes1bi +=1
					else: #posición 1 un, posición 3 post
						beats1un +=1; beats1post += 1
						if lista[8*i + 1] == 1:
							golpes1un +=1
						if lista[8*i + 3] == 1:
							golpes1post +=1
					if lista[8*i + 6] ==1: #posición 5 y 7 bi
						golpes2bi += 1
						beats1bi +=2
						if lista[8*i + 5] == 1:
							golpes1bi +=1
						if lista[8*i + 7] == 1:
							golpes1bi +=1
					else: #posición 5 pre, posición 7 post
						beats1pre +=1; beats1post += 1
						if lista[8*i + 5] == 1:
							golpes1pre +=1
						if lista[8*i + 7] == 1:
							golpes1post +=1
				else: #no golpe en nivel 3, posición 2 un, posición 6 post
					beats2un +=1; beats2post+= 1
					if lista[8*i +2] == 1: #posición 1 post, posición 3 pre
						golpes2un +=1
						beats1post +=1; beats1pre += 1
						if lista[8*i + 1] == 1:
							golpes1post +=1
						if lista[8*i + 3] == 1:
							golpes1pre +=1
					else: #posición 1 y 3 un
						beats1un +=2
						if lista[8*i + 1] == 1:
							golpes1un +=1
						if lista[8*i + 3] == 1:
							golpes1un +=1
					if lista[8*i + 6] ==1: #posición 5 post, posición 7 bi
						golpes2post += 1
						beats1post +=1; beats1bi += 1
						if lista[8*i + 5] == 1:
							golpes1post +=1
						if lista[8*i + 7] == 1:
							golpes1bi +=1
					else: #posición 5 un, posición 7 post
						beats1un +=1; beats1post += 1
						if lista[8*i + 5] == 1:
							golpes1un +=1
						if lista[8*i + 7] == 1:
							golpes1post +=1
			else: #nivel 3 un
				beats3un += 1
				if lista[8*i +4] == 1: #posición 2 post, posición 6 pre
					golpes3un +=1
					beats2post +=1; beats2pre += 1
					if lista[8*i +2] == 1: #posición 1 post, posición 3 bi
						golpes2post +=1
						beats1post +=1; beats1bi += 1
						if lista[8*i + 1] == 1:
							golpes1post +=1
						if lista[8*i + 3] == 1:
							golpes1bi +=1
					else: #posición 1 un, posición 3 post
						beats1un +=1; beats1post += 1
						if lista[8*i + 1] == 1:
							golpes1un +=1
						if lista[8*i + 3] == 1:
							golpes1post +=1
					if lista[8*i + 6] ==1: #posición 5 bi, posición 7 pre
						golpes2pre += 1
						beats1bi +=1; beats1pre += 1
						if lista[8*i + 5] == 1:
							golpes1bi +=1
						if lista[8*i + 7] == 1:
							golpes1pre +=1
					else: #posición 5 pre, posición 7 un
						beats1pre +=1; beats1un += 1
						if lista[8*i + 5] == 1:
							golpes1pre +=1
						if lista[8*i + 7] == 1:
							golpes1un +=1
				else: #posición 2 y 6 un
					beats2un +=2
					if lista[8*i +2] == 1: #posición 1 post, posición 3 pre
						golpes2un +=1
						beats1post +=1; beats1pre += 1
						if lista[8*i + 1] == 1:
							golpes1post +=1
						if lista[8*i + 3] == 1:
							golpes1pre +=1
					else: # posición 1 y 3 un
						beats1un +=2
						if lista[8*i + 1] == 1:
							golpes1un +=1
						if lista[8*i + 3] == 1:
							golpes1un +=1
					if lista[8*i + 6] ==1: #posición 5 post, posición 7 pre
						golpes2un += 1
						beats1post +=1; beats1pre += 1
						if lista[8*i + 5] == 1:
							golpes1post +=1
						if lista[8*i + 7] == 1:
							golpes1pre +=1
					else: #posiciónes 5 y 7 un
						beats1un +=2
						if lista[8*i + 5] == 1:
							golpes1un +=1
						if lista[8*i + 7] == 1:
							golpes1un +=1
	return [[p4, float(golpes3un)/max(beats3un, 0.5), float(golpes3pre)/max(beats3pre, 0.5), float(golpes3post)/max(beats3post, 0.5), float(golpes3bi)/max(beats3bi, 0.5), float(golpes2un)/max(beats2un,0.5), float(golpes2pre)/max(beats2pre, 0.5), float(golpes2post)/max(beats2post, 0.5), float(golpes2bi)/max(beats2bi, 0.5), float(golpes1un)/max(beats1un, 0.5), float(golpes1pre)/max(beats1pre,0.5), float(golpes1post)/max(beats1post,0.5), float(golpes1bi)/max(beats1bi, 0.5)], [p4*n/8, golpes3un, golpes3pre, golpes3post, golpes3bi, golpes2un, golpes2pre, golpes2post, golpes2bi, golpes1un, golpes1pre, golpes1post, golpes1bi], [n/8,beats3un, beats3pre, beats3post, beats3bi, beats2un, beats2pre, beats2post, beats2bi, beats1un, beats1pre, beats1post, beats1bi]]


def parametrosM644(lista):
	contador = 0
	tiraaux = [i%8 for i, j in enumerate(lista) if j == 1]  #tira con la posición en el compás de cada ataque. 
	naux = len(tiraaux)
	matriz = numpy.zeros((8,8)) #matriz de transición
	for i in range(len(tiraaux)-1):
		matriz[tiraaux[i], tiraaux[i+1]] +=1 #una transición. considero mod 8 para agrupar los intervalos interataque de más de un compás 
	for j in range(8):
		if sum(matriz[j,:]) != 0:
			matriz[j,:] =  matriz[j,:]/sum(matriz[j,:]) #normalizo
	return matriz

#MODELO NUEVO: Jerárquico refinado

#Modelo más refinado "Refinamiento total"
def parametrosMtotal44(lista):
	p4 = numpy.mean(lista[0:-1:8]) #otra vez la proba de nivel 4
	n = len(lista) -1
	beats1un = 0; beats1pre = 0; beats1post = 0; beats1bi = 0 #ahora los numeros refieren a posición, no a nivel
	beats2un = 0; beats2pre = 0; beats2post = 0; beats2bi = 0 
	beats3un = 0; beats3pre = 0; beats3post = 0; beats3bi = 0  
	beats4un = 0; beats4pre = 0; beats4post = 0; beats4bi = 0 
	beats5un = 0; beats5pre = 0; beats5post = 0; beats5bi = 0
	beats6un = 0; beats6pre = 0; beats6post = 0; beats6bi = 0  
	beats7un = 0; beats7pre = 0; beats7post = 0; beats7bi = 0 
	golpes1un = 0; golpes1pre = 0; golpes1post = 0; golpes1bi = 0
	golpes2un = 0; golpes2pre = 0; golpes2post = 0; golpes2bi = 0
	golpes3un = 0; golpes3pre = 0; golpes3post = 0; golpes3bi = 0
	golpes4un = 0; golpes4pre = 0; golpes4post = 0; golpes4bi = 0
	golpes5un = 0; golpes5pre = 0; golpes5post = 0; golpes5bi = 0
	golpes6un = 0; golpes6pre = 0; golpes6post = 0; golpes6bi = 0
	golpes7un = 0; golpes7pre = 0; golpes7post = 0; golpes7bi = 0
	###SEGUIR
	for i in range(n/8): #obs que uso division entera
		if lista[8*i] == 1: #posición 4 pre o bi
			if lista[8*(i+1)] == 1: #nivel 3 bi
				beats4bi += 1 
				if lista[8*i +4] == 1:#golpe en nivel 3
					golpes4bi +=1
					beats6bi += 1 #posición 6, beat bianclado
					beats2bi += 1 #posición 2, beat bianclado
					if lista[8*i +2] == 1: #posición 1 y 3 bi
						golpes2bi += 1
						beats1bi +=1
						beats3bi +=1
						if lista[8*i + 1] == 1:
							golpes1bi +=1
						if lista[8*i + 3] == 1:
							golpes3bi +=1
					else: #posición 1 pre, posición 3 post
						beats1pre +=1; beats3post +=1
						if lista[8*i + 1] == 1:
							golpes1pre +=1
						if lista[8*i + 3] == 1:
							golpes3post +=1
					if lista[8*i + 6] ==1: #posición 5 y 7 bi
						golpes6bi += 1
						beats5bi +=1
						beats7bi += 1
						if lista[8*i + 5] == 1:
							golpes5bi +=1
						if lista[8*i + 7] == 1:
							golpes7bi +=1
					else: #posición 5 pre, posición 7 post  ACAAAAA
						beats5pre +=1; beats7post +=1
						if lista[8*i + 5] == 1:
							golpes5pre +=1
						if lista[8*i + 7] == 1:
							golpes7post +=1
				else: #no golpe en lv 3, beats de posición 2 pre y de posición 6 post
					beats2pre +=1
					beats6post += 1
					if lista[8*i +2] == 1: #posición 1 bi, posición 3 pre
						golpes2pre += 1
						beats1bi +=1; beats3pre +=1
						if lista[8*i + 1] == 1:
							golpes1bi +=1
						if lista[8*i + 3] == 1:
							golpes3pre +=1
					else: #posición 1 pre, posición 3 un
						beats1pre +=1; beats3un +=1
						if lista[8*i + 1] == 1:
							golpes1pre +=1
						if lista[8*i + 3] == 1:
							golpes3un +=1
					if lista[8*i + 6] ==1: #posición 5 post, posición 7 bi
						golpes6post +=1
						beats7bi +=1; beats5post +=1
						if lista[8*i + 5] == 1:
							golpes5post +=1
						if lista[8*i + 7] == 1:
							golpes7bi +=1
					else: #posición 5 un, posición 7 post
						beats5un +=1; beats7post +=1
						if lista[8*i + 5] == 1:
							golpes5un +=1
						if lista[8*i + 7] == 1:
							golpes7post +=1
			else: #posición4 pre, posición 6 pre o un, posición 2 pre o bi
				beats4pre += 1
				if lista[8*i +4] == 1: 
					golpes4pre +=1 
					beats2bi +=1 #posición 2 bianclado
					beats6pre += 1 #posición 6 pre
					if lista[8*i +2] ==1: #posición 1 y 3 bi
						golpes2bi+=1
						beats1bi +=1
						beats3bi +=1
						if lista[8*i + 1] == 1:
							golpes1bi +=1
						if lista[8*i + 3] == 1:
							golpes3bi +=1
					else: #posición 1 pre, posición 3 post
						beats1pre +=1; beats3post +=1
						if lista[8*i + 1] == 1:
							golpes1pre +=1
						if lista[8*i + 3] == 1:
							golpes3post +=1
					if lista[8*i + 6] ==1: #posición 5 bi, posición 7 pre
						golpes6pre +=1
						beats5bi +=1; beats7pre += 1
						if lista[8*i + 5] == 1:
							golpes5bi +=1
						if lista[8*i + 7] == 1:
							golpes7pre +=1
					else: # posición 5 pre, posición 7 un
						beats5pre +=1; beats7un +=1
						if lista[8*i + 5] == 1:
							golpes5pre +=1
						if lista[8*i + 7] == 1:
							golpes7un +=1
				else: #no golpes en nivel 3. posición 2 pre, posición 6 un
					beats2pre +=1
					beats6un += 1 #posición 6 pre
					if lista[8*i +2] ==1: #posición 1 bi, posición 3 pre
						golpes2pre+=1
						beats1bi +=1; beats3pre += 1
						if lista[8*i + 1] == 1:
							golpes1bi +=1
						if lista[8*i + 3] == 1:
							golpes3pre +=1
					else: #posición 1 pre, posición 3 un
						beats3un +=1; beats1pre += 1
						if lista[8*i + 1] == 1:
							golpes1pre +=1
						if lista[8*i + 3] == 1:
							golpes3un +=1
					if lista[8*i + 6] ==1: #posición 5 post, posición 7 pre
						golpes6un +=1
						beats5post +=1; beats7pre += 1
						if lista[8*i + 5] == 1:
							golpes5post +=1
						if lista[8*i + 7] == 1:
							golpes7pre +=1
					else: #posición 5 un, posición 7 un
						beats5un +=1
						beats7un +=1
						if lista[8*i + 5] == 1:
							golpes5un +=1
						if lista[8*i + 7] == 1:
							golpes7un +=1
		else: # nivel 3 un o post
			if lista[8*(i+1)] == 1: #nivel 3 post
				beats4post += 1
				if lista[8*i +4] == 1: #posición 2 post, posición 6 bi
					golpes4post +=1
					beats2post +=1; beats6bi+= 1
					if lista[8*i +2] == 1: #posición 1 post, posición 3 bi
						golpes2post +=1
						beats1post +=1; beats3bi += 1
						if lista[8*i + 1] == 1:
							golpes1post +=1
						if lista[8*i + 3] == 1:
							golpes3bi +=1
					else: #posición 1 un, posiciónn 3 post
						beats1un +=1; beats3post += 1
						if lista[8*i + 1] == 1:
							golpes1un +=1
						if lista[8*i + 3] == 1:
							golpes3post +=1
					if lista[8*i + 6] ==1: #posición 5 y 7 bi
						golpes6bi += 1
						beats5bi +=1
						beats7bi +=1
						if lista[8*i + 5] == 1:
							golpes5bi +=1
						if lista[8*i + 7] == 1:
							golpes7bi +=1
					else: #posición 5 pre, posición 7 post
						beats5pre +=1; beats7post += 1
						if lista[8*i + 5] == 1:
							golpes5pre +=1
						if lista[8*i + 7] == 1:
							golpes7post +=1
				else: #no golpe en nivel 3, posición 2 un, posición 6 post
					beats2un +=1; beats6post += 1
					if lista[8*i +2] == 1: #posición 1 post, posición 3 pre
						golpes2un +=1
						beats1post +=1; beats3pre += 1
						if lista[8*i + 1] == 1:
							golpes1post +=1
						if lista[8*i + 3] == 1:
							golpes3pre +=1
					else: #posición 1 y 3 un
						beats1un +=1
						beats3un +=1
						if lista[8*i + 1] == 1:
							golpes1un +=1
						if lista[8*i + 3] == 1:
							golpes3un +=1
					if lista[8*i + 6] ==1: #posición 5 post, posición 7 bi
						golpes6post += 1
						beats5post +=1; beats7bi += 1
						if lista[8*i + 5] == 1:
							golpes5post +=1
						if lista[8*i + 7] == 1:
							golpes7bi +=1
					else: #posición 5 un, posición 7 post
						beats5un +=1; beats7post += 1
						if lista[8*i + 5] == 1:
							golpes5un +=1
						if lista[8*i + 7] == 1:
							golpes7post +=1
			else: #nivel 3 un
				beats4un += 1
				if lista[8*i +4] == 1: #posición 2 post, posición 6 pre
					golpes4un +=1
					beats2post +=1; beats6pre += 1
					if lista[8*i +2] == 1: #posición 1 post, posición 3 bi
						golpes2post +=1
						beats1post +=1; beats3bi += 1
						if lista[8*i + 1] == 1:
							golpes1post +=1
						if lista[8*i + 3] == 1:
							golpes3bi +=1
					else: #posición 1 un, posición 3 post
						beats1un +=1; beats3post += 1
						if lista[8*i + 1] == 1:
							golpes1un +=1
						if lista[8*i + 3] == 1:
							golpes3post +=1
					if lista[8*i + 6] ==1: #posición 5 bi, posición 7 pre
						golpes6pre += 1
						beats5bi +=1; beats7pre += 1
						if lista[8*i + 5] == 1:
							golpes5bi +=1
						if lista[8*i + 7] == 1:
							golpes7pre +=1
					else: #posición 5 pre, posición 7 un
						beats5pre +=1; beats7un += 1
						if lista[8*i + 5] == 1:
							golpes5pre +=1
						if lista[8*i + 7] == 1:
							golpes7un +=1
				else: #posición 2 y 6 un
					beats2un +=1
					beats6un +=1
					if lista[8*i +2] == 1: #posición 1 post, posición 3 pre
						golpes2un +=1
						beats1post +=1; beats3pre += 1
						if lista[8*i + 1] == 1:
							golpes1post +=1
						if lista[8*i + 3] == 1:
							golpes3pre +=1
					else: # posición 1 y 3 un
						beats1un +=1
						beats3un +=1
						if lista[8*i + 1] == 1:
							golpes1un +=1
						if lista[8*i + 3] == 1:
							golpes3un +=1
					if lista[8*i + 6] ==1: #posición 5 post, posición 7 pre
						golpes6un += 1
						beats5post +=1; beats7pre += 1
						if lista[8*i + 5] == 1:
							golpes5post +=1
						if lista[8*i + 7] == 1:
							golpes7pre +=1
					else: #posiciónes 5 y 7 un
						beats5un +=1
						beats7un +=1
						if lista[8*i + 5] == 1:
							golpes5un +=1
						if lista[8*i + 7] == 1:
							golpes7un +=1
	return [[p4, float(golpes1un)/max(beats1un,0.5), float(golpes1pre)/max(beats1pre,0.5), float(golpes1post)/max(beats1post,0.5), float(golpes1bi)/max(beats1bi,0.5), float(golpes2un)/max(beats2un,0.5), float(golpes2pre)/max(beats2pre,0.5), float(golpes2post)/max(beats2post,0.5), float(golpes2bi)/max(beats2bi,0.5), float(golpes3un)/max(beats3un,0.5), float(golpes3pre)/max(beats3pre,0.5), float(golpes3post)/max(beats3post,0.5), float(golpes3bi)/max(beats3bi,0.5), float(golpes4un)/max(beats4un,0.5), float(golpes4pre)/max(beats4pre,0.5), float(golpes4post)/max(beats4post,0.5), float(golpes4bi)/max(beats4bi,0.5), float(golpes5un)/max(beats5un,0.5), float(golpes5pre)/max(beats5pre,0.5), float(golpes5post)/max(beats5post,0.5), float(golpes5bi)/max(beats5bi,0.5),float(golpes6un)/max(beats6un,0.5), float(golpes6pre)/max(beats6pre, 0.5), float(golpes6post)/max(beats6post,0.5), float(golpes6bi)/max(beats6bi,0.5),float(golpes7un)/max(beats7un,0.5), float(golpes7pre)/max(beats7pre,0.5), float(golpes7post)/max(beats7post,0.5), float(golpes7bi)/max(beats7bi,0.5)], [p4*n/8, golpes1un, golpes1pre, golpes1post, golpes1bi, golpes2un, golpes2pre, golpes2post, golpes2bi, golpes3un, golpes3pre, golpes3post, golpes3bi, golpes4un, golpes4pre, golpes4post, golpes4bi, golpes5un, golpes5pre, golpes5post, golpes5bi, golpes6un, golpes6pre, golpes6post, golpes6bi, golpes7un, golpes7pre, golpes7post, golpes7bi], [n/8, beats1un, beats1pre, beats1post, beats1bi, beats2un, beats2pre, beats2post, beats2bi, beats3un, beats3pre, beats3post, beats3bi, beats4un, beats4pre, beats4post, beats4bi, beats5un, beats5pre, beats5post, beats5bi, beats6un, beats6pre, beats6post, beats6bi, beats7un, beats7pre, beats7post, beats7bi]]

#uso los calculos del refinamiento total para definir pM7 (obs que asi podría definirse pM5 tambien)

def parametrosM744(lista): #orden: [IIII, 1,3,5,7,II,III]
	parametrosaux = parametrosMtotal44(lista)
	golpesfinos = numpy.array(parametrosaux[1], dtype = numpy.float); beatsfinos = numpy.array(parametrosaux[2], dtype = numpy.float)
	indices = [0,1,2,3,4,9,10,11,12,17,18,19,20,25,26,27,28]
	golpesagrup = [golpesfinos[5] + golpesfinos[21], golpesfinos[6] + golpesfinos[22], golpesfinos[7] + golpesfinos[23], golpesfinos[8] + golpesfinos[24], golpesfinos[13], golpesfinos[14], golpesfinos[15], golpesfinos[16]]
	golpes = numpy.append(golpesfinos[indices], golpesagrup)
	beatsagrup = [beatsfinos[5] + beatsfinos[21], beatsfinos[6] + beatsfinos[22], beatsfinos[7] + beatsfinos[23], beatsfinos[8] + beatsfinos[24], beatsfinos[13], beatsfinos[14], beatsfinos[15], beatsfinos[16]]
	beats = numpy.append(beatsfinos[indices], beatsagrup)
	cociente = golpes/beats; cociente;  cociente[numpy.isnan(cociente)] = 0 #limpio los nan
	return [cociente, golpes, beats]


#Funciones especificas para 2/4


#Modelo 1: hallo la proporción de 1s total. 


#Modelo 3: Hallo las probas de ataque de cada nivel (3 niveles)
def parametrosM324(lista):
	beatsnivel3 = lista[0:-1:4] #excluye al ultimo 1
	beatsnivel2 = lista[2::4]
	beatsnivel1 = lista[1::2]
	return [numpy.mean(beatsnivel3), numpy.mean(beatsnivel2), numpy.mean(beatsnivel1)]


#Modelo 4: hallo las probas de ataque de cada posición

def parametrosM424(lista):
	salida = [0,0,0,0]
	for k in range(4):
		salida[k] = numpy.mean(lista[k::4])
	return salida

#Modelo 5: hallo las probas de los distintos tipos de anclaje y distintos niveles. En total son 9.

def parametrosM524(lista):#devuelve [[probas], [golpes]]
	p3 = numpy.mean(lista[0:-1:4]) #otra vez la proba de nivel 3
	n = len(lista) -1
	beats1un = 0; beats1pre = 0; beats1post = 0; beats1bi = 0 
	beats2un = 0; beats2pre = 0; beats2post = 0; beats2bi = 0 
	golpes1un = 0; golpes1pre = 0; golpes1post = 0; golpes1bi = 0
	golpes2un = 0; golpes2pre = 0; golpes2post = 0; golpes2bi = 0
	for i in range(n/4): #obs que uso division entera
		if lista[4*i] == 1: #nivel 2 pre o bi
			if lista[4*(i+1)] == 1: #nivel 2 bi
				beats2bi += 1 
				if lista[4*i +2] == 1:#golpe en nivel 2
					golpes2bi +=1
					beats1bi += 2 #posición 1 y 3, beat bianclado
					if lista[4*i +1] == 1:
						golpes1bi += 1
					if lista[4*i + 3] ==1:
						golpes1bi += 1
				else: #no golpe en lv 2, beats de posición 1 pre y de posición 3 post
					beats1pre +=1
					beats1post += 1
					if lista[4*i +1] == 1: 
						golpes1pre += 1
					if lista[4*i + 3] ==1: 
						golpes1post +=1
			else: 
				beats2pre += 1
				if lista[4*i +2] == 1: 
					golpes2pre +=1 
					beats1bi +=1 #posición 1 bianclado
					beats1pre += 1 #posición 3 pre
					if lista[4*i +1] ==1: 
						golpes1bi+=1
					if lista[4*i + 3] ==1: #posición 5 bi, posición 7 pre
						golpes1pre +=1
				else: #no golpes en nivel 2
					beats1pre +=1
					beats1un += 1 
					if lista[4*i +1] ==1:
						golpes1pre+=1
					if lista[4*i + 3] ==1: #posición 5 post, posición 7 pre
						golpes1un +=1
		else: # nivel 3 un o post
			if lista[4*(i+1)] == 1: #nivel 2 post
				beats2post += 1
				if lista[4*i +2] == 1: #posición 2 post, posición 6 bi
					golpes2post +=1
					beats1post +=1; beats1bi+= 1
					if lista[4*i +1] == 1: 
						golpes1post +=1
					if lista[4*i + 3] ==1: 
						golpes1bi += 1
				else: 
					beats1un +=1; beats1post+= 1
					if lista[4*i +1] == 1: 
						golpes1un +=1
					if lista[4*i + 3] ==1: 
						golpes1post += 1
			else: #nivel 2 un
				beats2un += 1
				if lista[4*i +2] == 1: 
					golpes2un +=1
					beats1post +=1; beats1pre += 1
					if lista[4*i +1] == 1:
						golpes1post +=1
					if lista[4*i + 3] ==1:
						golpes1pre += 1
				else: 
					beats1un +=2
					if lista[4*i +1] == 1: #posición 1 post, posición 3 pre
						golpes1un +=1
					if lista[4*i + 3] ==1: #posición 5 post, posición 7 pre
						golpes1un += 1
	return [[p3, float(golpes2un)/max(beats2un,0.5), float(golpes2pre)/max(beats2pre,0.5), float(golpes2post)/max(beats2post,0.5), float(golpes2bi)/max(beats2bi,0.5), float(golpes1un)/max(beats1un,0.5), float(golpes1pre)/max(beats1pre,0.5), float(golpes1post)/max(beats1post,0.5), float(golpes1bi)/max(beats1bi,0.5)], [p3*n/4, golpes2un, golpes2pre, golpes2post, golpes2bi, golpes1un, golpes1pre, golpes1post, golpes1bi], [n/4, beats2un, beats2pre, beats2post, beats2bi, beats1un, beats1pre, beats1post, beats1bi]]


def parametrosM624(lista):
	contador = 0
	tiraaux = [i%4 for i, j in enumerate(lista) if j == 1]  #tira con la posición en el compas de cada ataque. Obs que no distingue largos de cortos
	naux = len(tiraaux)
	matriz = numpy.zeros((4,4)) #matriz de transicion
	for i in range(len(tiraaux)-1):
		matriz[tiraaux[i], tiraaux[i+1]] +=1 #una transicion. considero mod 4 para agrupar los interonset de mas de un compas 
	for j in range(4):
		if sum(matriz[j,:]) != 0:
			matriz[j,:] =  matriz[j,:]/sum(matriz[j,:]) #normalizo
	return matriz

###MODELO 7, jerarquico refinado total

def parametrosM724(lista):#devuelve [[probas], [golpes]]
	p3 = numpy.mean(lista[0:-1:4]) #otra vez la proba de nivel 3
	n = len(lista) -1
	beats1unfd = 0; beats1prefd = 0; beats1postfd = 0; beats1bifd = 0 
	beats1undf = 0; beats1predf = 0; beats1postdf = 0; beats1bidf = 0 
	beats2un = 0; beats2pre = 0; beats2post = 0; beats2bi = 0 
	golpes1unfd = 0; golpes1prefd = 0; golpes1postfd = 0; golpes1bifd = 0
	golpes1undf = 0; golpes1predf = 0; golpes1postdf = 0; golpes1bidf = 0
	golpes2un = 0; golpes2pre = 0; golpes2post = 0; golpes2bi = 0
	for i in range(n/4): #obs que uso division entera
		if lista[4*i] == 1: #nivel 2 pre o bi
			if lista[4*(i+1)] == 1: #nivel 2 bi
				beats2bi += 1 
				if lista[4*i +2] == 1:#golpe en nivel 2
					golpes2bi +=1
					beats1bifd += 1 #posición 1 y 3, beat bianclado
					beats1bidf +=1
					if lista[4*i +1] == 1:
						golpes1bifd += 1
					if lista[4*i + 3] ==1:
						golpes1bidf += 1
				else: #no golpe en lv 2, beats de posición 1 pre y de posición 3 post
					beats1prefd +=1
					beats1postdf += 1
					if lista[4*i +1] == 1: 
						golpes1prefd += 1
					if lista[4*i + 3] ==1: 
						golpes1postdf +=1
			else: 
				beats2pre += 1
				if lista[4*i +2] == 1: 
					golpes2pre +=1 
					beats1bifd +=1 #posición 1 bianclado
					beats1predf += 1 #posición 3 pre
					if lista[4*i +1] ==1: 
						golpes1bifd+=1
					if lista[4*i + 3] ==1: #posición 5 bi, posición 7 pre
						golpes1predf +=1
				else: #no golpes en nivel 2
					beats1prefd +=1
					beats1undf += 1 
					if lista[4*i +1] ==1:
						golpes1prefd+=1
					if lista[4*i + 3] ==1: #posición 5 post, posición 7 pre
						golpes1undf +=1
		else: 
			if lista[4*(i+1)] == 1: #nivel 2 post
				beats2post += 1
				if lista[4*i +2] == 1: 
					golpes2post +=1
					beats1postfd +=1; beats1bidf+= 1
					if lista[4*i +1] == 1: 
						golpes1postfd +=1
					if lista[4*i + 3] ==1: 
						golpes1bidf += 1
				else: 
					beats1unfd +=1; beats1postdf+= 1
					if lista[4*i +1] == 1: 
						golpes1unfd +=1
					if lista[4*i + 3] ==1: 
						golpes1postdf += 1
			else: #nivel 2 un
				beats2un += 1
				if lista[4*i +2] == 1: 
					golpes2un +=1
					beats1postfd +=1; beats1predf += 1
					if lista[4*i +1] == 1:
						golpes1postfd +=1
					if lista[4*i + 3] ==1:
						golpes1predf += 1
				else: 
					beats1unfd +=1
					beats1undf +=1
					if lista[4*i +1] == 1: #posición 1 post, posición 3 pre
						golpes1unfd +=1
					if lista[4*i + 3] ==1: #posición 5 post, posición 7 pre
						golpes1undf += 1
	return [[p3, float(golpes2un)/max(beats2un, 0.5), float(golpes2pre)/max(beats2pre, 0.5), float(golpes2post)/max(beats2post,0.5), float(golpes2bi)/max(beats2bi, 0.5), float(golpes1unfd)/max(beats1unfd,0.5), float(golpes1prefd)/max(beats1prefd, 0.5), float(golpes1postfd)/max(beats1postfd, 0.5), float(golpes1bifd)/max(beats1bifd, 0.5), float(golpes1undf)/max(beats1undf,0.5), float(golpes1predf)/max(beats1predf, 0.5), float(golpes1postdf)/max(beats1postdf, 0.5), float(golpes1bidf)/max(beats1bidf, 0.5)], [p3*n/4, golpes2un, golpes2pre, golpes2post, golpes2bi, golpes1unfd, golpes1prefd, golpes1postfd, golpes1bifd, golpes1undf, golpes1predf, golpes1postdf, golpes1bidf], [n/4, beats2un, beats2pre, beats2post, beats2bi, beats1unfd, beats1prefd, beats1postfd, beats1bifd,beats1undf, beats1predf, beats1postdf, beats1bidf]]
	#divido entre max(beats, 0.5) para que el denominador no se anule


