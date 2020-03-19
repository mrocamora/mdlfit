# encoding: utf-8
from music21 import *
import copy
import numpy
from auxiliares import escribir
import os


###FUNCIONES PARA OBTENER LAS SECUENCIAS RITMICAS DE LOS CORPUS EN music21
#VERSIÖN MODIFICADA PARA EXTRAER COMPASES "SUELTOS" QUE ESTEN EN EL COMPÁS DESEADO


#Para 4/4 con beats de corchea


def corpusobras44(nombrecorpus): #nombrecorpus es un string con el nombre del corpus en music21, por ej 'EssenFolksong'
	bpc = 8 #beats por compas
	#nombrecorpus = 'EssenFolksong' #Se puede elegir cualquier corpus de music21
	#nombrecorpus = 'airdsAirs'
	#nombrecorpus = 'oneills1850'
	corpusobras = corpus.getComposer(nombrecorpus)
	listagolpes = []
	listanumeros = []
	for ruta in corpusobras:
		indice = 0  #para ir guardando en las obras que pueden no ser sucesivas
		op = converter.parse(ruta)
		if op.hasElementOfClass('Score'): #es posiblemente un Opus. Hay muchos Scores dentro y hay que iterar
			numeros = [x for x in op.getNumbers() if x not in listanumeros]
			listagolpesobra = len(numeros)*[[]] #me preparo para guardar, a lo sumo, algo de todas las obras
			for i in range(len(numeros)): #por si los numeros no son todos secuenciales
				obrita = op.scores[i] #NO FLAT. Si aplano pierdo la estructura de los compases
				obrita = obrita.parts[0]
				compases = obrita.getElementsByClass('Measure')
				ncompas = len(compases)
				golpesobrita = (bpc*ncompas +1)*[0] #Por si acaso
				lugar = 0;  #para ir guardando los compases que pueden no ser sucesivos.
				for l in range(ncompas): #itero en los compases
					compasactual = compases[l].flat.notes #Aun tengo que decidir si me quedo con el compás o no
					lugaresgolpes = [((x.beat -1)/0.5)  for x in compasactual if x.getContextByClass('TimeSignature') != None]
					guardarcompas = False
					if lugaresgolpes == [] or  min([x.is_integer() for x in lugaresgolpes ]) == 0: #i.e algo ocurre en un beat fuera de la grilla, o el compás es vacio. 
						pass
					else:
						largocompas = len(compasactual)
						guardarcompas = True
						for j in range(largocompas):
							TS = compasactual[j].getContextByClass('TimeSignature')
							if TS != None and TS.numerator == 4 and TS.denominator == 4:  #estoy en 4/4
								pass
							else:
								guardarcompas = False
						if guardarcompas:
							golpescompas = numpy.array(bpc*[0]); golpesenteros = [int(x) for x in lugaresgolpes]
							golpescompas[golpesenteros] = 1
							golpesobrita[lugar:lugar+bpc] = golpescompas
							lugar += bpc #nuevo compás a guardar
				if lugar > bpc: #ie, guarde más de un compás en golpesobrita
					if golpesobrita[lugar-bpc:lugar] == [1,0,0,0,0,0,0,0]: #termina con un solo golpe en el primer beat. No agrego nada, saco los ultimos 7 ceros por coherencia
						golpesobrita = golpesobrita[:lugar -bpc +1]
					else:
						golpesobrita[lugar] = 1 #el 1 al final de la obra 
						golpesobrita = golpesobrita[:lugar +1 ]
					listagolpesobra[indice] = golpesobrita 
					indice +=1
			listagolpesobra = listagolpesobra[:indice]
			listagolpes.extend(listagolpesobra)
		elif op.hasElementOfClass('Part'): #trabajo directo con la obra
			obrita = op.parts[0]
			compases = obrita.getElementsByClass('Measure')
			ncompas = len(compases)
			golpesobrita = (bpc*ncompas +1)*[0] #Nuevamente defino lista con largo más que suficiente
			lugar = 0;  #para ir guardando los compases que pueden no ser sucesivos.
			for l in range(ncompas): #itero en los compases
				compasactual = compases[l].flat.notes #Aun hay que decidir si guardar el compás o no
				lugaresgolpes = [((x.beat -1)/0.5)  for x in compasactual if x.getContextByClass('TimeSignature') != None]
				guardarcompas = False
				if lugaresgolpes == [] or  min([x.is_integer() for x in lugaresgolpes ]) == 0: #i.e algo ocurre en un beat fuera de la grilla, o el compás es vacio. 
					pass
				else:
					largocompas = len(compasactual)
					guardarcompas = True
					for j in range(largocompas):
						TS = compasactual[j].getContextByClass('TimeSignature')
						if TS != None and TS.numerator == 4 and TS.denominator == 4:  #estoy en 4/4
							pass
						else:
							guardarcompas = False
					if guardarcompas:
						golpescompas = numpy.array(bpc*[0]); golpesenteros = [int(x) for x in lugaresgolpes]
						golpescompas[golpesenteros] = 1
						golpesobrita[lugar:lugar+bpc] = golpescompas
						lugar += bpc #nuevo compás a guardar
			if lugar >bpc: #esto es, guarde más de un compás en golpesobrita
				if golpesobrita[lugar - bpc: lugar] == [1,0,0,0,0,0,0,0]: #termina con un solo golpe en el primer beat. No agrego nada, saco los ultimos 7 ceros por coherencia
					golpesobrita = golpesobrita[:lugar -bpc +1]
				else:
					golpesobrita[lugar] = 1 #agrego un 1 al final de la obra por cuestión de formato
					golpesobrita = golpesobrita[:lugar +1 ]
				listagolpes.append(golpesobrita) #agrego golpesobrita sólo si es pertinente
		else: #cualquier otro contenedor raro, lo omito
			print 'ATENCIÓN: el objeto en ' + ruta + ' es de un tipo no usual. Se omite.'
	if [] in listagolpes:
		listagolpes = listagolpes[:listagolpes.index([])] #saco las listas vacías que me quedaron
	#las ultimas 8 obras de Aird's Airs en 4/4 son duos y music 21 los representa como una melodía dos veces. elimino estas obras
	if nombrecorpus == 'airdsAirs':
		listagolpes = listagolpes[:-8]
	escribir(listagolpes, 'golpes' + nombrecorpus+ '44')


def corpusobras24(nombrecorpus):
	bpc = 4
	#nombrecorpus = 'EssenFolksong' #se puede elegir otro corpus de music21
	#nombrecorpus = 'airdsAirs'
	nombrecorpus = 'oneills1850'
	corpusobras = corpus.getComposer(nombrecorpus)
	listagolpes = []
	listanumeros = []
	for ruta in corpusobras:
		indice = 0  #para ir guardando en las obras que pueden no ser sucesivas
		op = converter.parse(ruta)
		if op.hasElementOfClass('Score'): #es posiblemente un Opus. Hay muchos Scores dentro y hay que iterar
			numeros = [x for x in op.getNumbers() if x not in listanumeros] #para evitar repeticiones 
			listagolpesobra = len(numeros)*[[]] #me preparo para guardar, a lo sumo, algo de todas las obras
			for i in range(len(numeros)): #por si los numeros no son todos secuenciales
				obrita = op.scores[i] #NO FLAT. Si aplano pierdo la estructura de los compases
				obrita = obrita.parts[0]
				compases = obrita.getElementsByClass('Measure')
				ncompas = len(compases)
				golpesobrita = (bpc*ncompas +1)*[0] #Nuevamente defino lista con largo más que suficiente
				lugar = 0;  #para ir guardando los compases que pueden no ser sucesivos.
				for l in range(ncompas): #itero en los compases
					compasactual = compases[l].flat.notes #Aun hay que decidir si guardar el compás o no
					lugaresgolpes = [((x.beat -1)/0.5)  for x in compasactual if x.getContextByClass('TimeSignature') != None]
					guardarcompas = False
					if lugaresgolpes == [] or  min([x.is_integer() for x in lugaresgolpes ]) == 0: #i.e algo ocurre en un beat fuera de la grilla, o el compás es vacio. 
						pass
					else:
						largocompas = len(compasactual)
						guardarcompas = True
						for j in range(largocompas):
							TS = compasactual[j].getContextByClass('TimeSignature')
							if TS != None and TS.numerator == 2 and TS.denominator == 4:  #estoy en 2/4
								pass
							else:
								guardarcompas = False
						if guardarcompas:
							golpescompas = numpy.array(bpc*[0]); golpesenteros = [int(x) for x in lugaresgolpes]
							golpescompas[golpesenteros] = 1
							golpesobrita[lugar:lugar+bpc] = golpescompas
							lugar += bpc #nuevo compás a guardar
				if lugar >bpc: #esto es, guarde más de un compás en golpesobrita
					if golpesobrita[lugar-bpc:lugar] == [1,0,0,0]: #termina con un solo golpe en el primer beat. No agrego nada, saco los ultimos 3 ceros por coherencia
						golpesobrita = golpesobrita[:lugar -bpc + 1]
					else:
						golpesobrita[lugar] = 1 #agrego un 1 al final de la obra por cuestión de formato
						golpesobrita = golpesobrita[:lugar +1 ]
					listagolpesobra[indice] = golpesobrita 
					indice +=1
			listagolpesobra = listagolpesobra[:indice]
			listagolpes.extend(listagolpesobra)
		elif op.hasElementOfClass('Part'): #trabajo directo con la obra
			obrita = op.parts[0]
			compases = obrita.getElementsByClass('Measure')
			ncompas = len(compases)
			golpesobrita = (bpc*ncompas +1)*[0] #Nuevamente defino lista con largo más que suficiente
			lugar = 0;  #para ir guardando los compases que pueden no ser sucesivos.
			for l in range(ncompas): #itero en los compases
				compasactual = compases[l].flat.notes #Aun hay que decidir si guardar el compás o no
				lugaresgolpes = [((x.beat -1)/0.5)  for x in compasactual if x.getContextByClass('TimeSignature') != None]
				guardarcompas = False
				if lugaresgolpes == [] or  min([x.is_integer() for x in lugaresgolpes ]) == 0: #i.e algo ocurre en un beat fuera de la grilla, o el compás es vacio. 
					pass
				else:
					largocompas = len(compasactual)
					guardarcompas = True
					for j in range(largocompas):
						TS = compasactual[j].getContextByClass('TimeSignature')
						if TS != None and TS.numerator == 2 and TS.denominator == 4:  #estoy en 2/4
							pass
						else:
							guardarcompas = False
					if guardarcompas:
						golpescompas = numpy.array(bpc*[0]); golpesenteros = [int(x) for x in lugaresgolpes]
						golpescompas[golpesenteros] = 1
						golpesobrita[lugar:lugar+bpc] = golpescompas; 
			if lugar > bpc: #esto es, guarde más de un compás en golpesobrita
				if golpesobrita[lugar-bpc: lugar] == [1,0,0,0]: #termina con un solo golpe en el primer beat. No agrego nada, saco los ultimos 3 ceros por coherencia
					golpesobrita = golpesobrita[:lugar-bpc +1]
				else:
					golpesobrita[lugar] = 1 #agrego un 1 al final de la obra por cuestión de formato
					golpesobrita = golpesobrita[:lugar +1 ]
				listagolpes.append(golpesobrita) #agrego golpesobrita sólo si es pertinente
		else: #cualquier otro contenedor raro, lo omito
			print 'ATENCIÓN: el objeto en ' + ruta + ' es de un tipo no usual. Se omite.'
	if [] in listagolpes:
		listagolpes = listagolpes[:listagolpes.index([])] #saco las listas vacías que me quedaron
	escribir(listagolpes, 'golpes' + nombrecorpus+ '24')

