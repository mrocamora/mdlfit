# coding = utf-8

#importar este modulo antes que nada

from music21 import *
import copy


diccionario = {0:'C', 1:'C#',2: 'D', 3: 'D#', 4:'E', 5 :'F', 6: 'F#' , 7: 'G', 8: 'G#' , 9: 'A',10: 'A#', 11: 'B', 12: 'rest' } #remanente de cuando no conocia pitchClass


#auxiliar: la funcion escribir
def escribir (matriz, nombredearchivo):
	salida = ''
	for fila in matriz:
		indicecolumna = 0
		for j in fila:
			if indicecolumna +1 < len(fila):  #i.e, si no estoy en el ultimo elemento
				salida = salida + str(j) + ' '
				indicecolumna += 1
			else:
				salida = salida + str(j) + '\n'
				indicecolumna +=1
	salida = salida + '\n' #otro salto de linea para indicar que termino
	mat = open(nombredearchivo + '.txt', 'wb')
	mat.write(salida)
	mat.close()


#escribir2, agrega al archivo en vez de sobreescribir

def escribir2 (matriz, nombredearchivo): #matriz es una lista de filas
	salida = ''
	for fila in matriz:
		indicecolumna = 0
		for j in fila:
			if indicecolumna +1 < len(fila):  #i.e, si no estoy en el ultimo elemento
				salida = salida + str(j) + ' '
				indicecolumna += 1
			else:
				salida = salida + str(j) + '\n'
				indicecolumna +=1
	mat = open(nombredearchivo + '.txt', 'a')
	mat.write(salida)
	mat.close()

#Restricciones al 25/12/16, con filename incorporado

def restricciones(coral, filenotas, filelargos): #los ultimos argumentos son los nombres de archivo de vecnotas y veclargos
	original = coral
	tono = original.analyze('key')
	tonica = note.Note()
	tonica.pitch = tono.pitchFromDegree(1)
	do = note.Note('C')
	intervalo = interval.Interval(tonica, do)		
	soprano = original.parts[0].getElementsByClass(stream.Measure)
	contralto = original.parts[1].getElementsByClass(stream.Measure)
	tenor = original.parts[2].getElementsByClass(stream.Measure)
	bajo = original.parts[3].getElementsByClass(stream.Measure)
	nsoprano = []
	ncontralto = []
	ntenor = []
	nbajo = []		
	restr_sop = []
	restr_cont = []
	restr_ten = []
	restr_bajo = []
	for compas in soprano:
		if len(compas.notes) >0:
			nsoprano.append(len(compas.notes))			
			if compas.notes[0].isChord:
				alturasmidi = [a.midi for a in compas.notes[0].pitches]
				superior = max(alturasmidi)
				alturaaux = note.Note()
				alturaaux.pitch.midi = superior
				nuevasop = alturaaux.transpose(intervalo).pitch
				restr_sop.append(nuevasop.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitches = compas.notes[0].transpose(intervalo).pitches
			else: #si es una nota comun
				nuevasop = compas.notes[0].transpose(intervalo).pitch
				restr_sop.append(nuevasop.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitch = nuevasop
			compas.notes[0].color = 'blue' 
	if len (soprano[-1].notes) > 1: #es decir si hay mas de una nota en el ultimo compas
		if soprano[-1].notes[-1].isChord:		
			alturasmidi = [a.midi for a in soprano[-1].notes[-1].pitches]
			superior = max(alturasmidi)
			alturaaux = note.Note()
			alturaaux.pitch.midi = superior
			nuevasop = alturaaux.transpose(intervalo).pitch
			restr_sop.append(nuevasop.pitchClass) #guardo la nota transportada a do
			soprano[-1].notes[-1].pitches = soprano[-1].notes[-1].transpose(intervalo).pitches
		else:
			nuevasop = soprano[-1].notes[-1].transpose(intervalo).pitch
			restr_sop.append(nuevasop.pitchClass) #la ultima nota
		soprano[-1].notes[-1].color = 'blue' 
		nsoprano.append(0) #para que el script en R no falle
	
	for compas in contralto:
		if len(compas.notes) >0:
			ncontralto.append(len(compas.notes))
			if compas.notes[0].isChord:
				alturasmidi = [a.midi for a in compas.notes[0].pitches]
				superior = max(alturasmidi)
				alturaaux = note.Note()
				alturaaux.pitch.midi = superior
				nuevacont = alturaaux.transpose(intervalo).pitch
				restr_cont.append(nuevacont.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitches = compas.notes[0].transpose(intervalo).pitches
			else: #si es una nota comun
				nuevacont = compas.notes[0].transpose(intervalo).pitch
				restr_cont.append(nuevacont.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitch = nuevacont
			compas.notes[0].color = 'blue'
	
	if len (contralto[-1].notes) > 1: #es decir si hay mas de una nota en el ultimo compas
		if contralto[-1].notes[-1].isChord:		
			alturasmidi = [a.midi for a in contralto[-1].notes[-1].pitches]
			superior = max(alturasmidi)
			alturaaux = note.Note()
			alturaaux.pitch.midi = superior
			nuevacont = alturaaux.transpose(intervalo).pitch
			restr_cont.append(nuevacont.pitchClass) #guardo la nota transportada a do
			contralto[-1].notes[-1].pitches = contralto[-1].notes[-1].transpose(intervalo).pitches
		else:
			nuevacont = contralto[-1].notes[-1].transpose(intervalo).pitch
			restr_cont.append(nuevacont.pitchClass) #la ultima nota
		contralto[-1].notes[-1].color = 'blue'
		ncontralto.append(0)
	for compas in tenor:
		if len(compas.notes) >0:
			ntenor.append(len(compas.notes))
			if compas.notes[0].isChord:
				alturasmidi = [a.midi for a in compas.notes[0].pitches]
				superior = max(alturasmidi)
				alturaaux = note.Note()
				alturaaux.pitch.midi = superior
				nuevaten = alturaaux.transpose(intervalo).pitch
				restr_ten.append(nuevaten.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitches = compas.notes[0].transpose(intervalo).pitches
			else: #si es una nota comun
				nuevaten = compas.notes[0].transpose(intervalo).pitch
				restr_ten.append(nuevaten.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitch = nuevaten
			compas.notes[0].color = 'blue'
	
	if len (tenor[-1].notes) > 1: #es decir si hay mas de una nota en el ultimo compas
		if tenor[-1].notes[-1].isChord:		
			alturasmidi = [a.midi for a in tenor[-1].notes[-1].pitches]
			superior = max(alturasmidi)
			alturaaux = note.Note()
			alturaaux.pitch.midi = superior
			nuevaten = alturaaux.transpose(intervalo).pitch
			restr_ten.append(nuevacont.pitchClass) #guardo la nota transportada a do
			tenor[-1].notes[-1].pitches = tenor[-1].notes[-1].transpose(intervalo).pitches
		else:
			nuevaten = tenor[-1].notes[-1].transpose(intervalo).pitch
			restr_ten.append(nuevaten.pitchClass) #la ultima nota
		tenor[-1].notes[-1].color = 'blue'
		ntenor.append(0)
	for compas in bajo:
		if len(compas.notes) >0:
			nbajo.append(len(compas.notes))
			if compas.notes[0].isChord:
				alturasmidi = [a.midi for a in compas.notes[0].pitches]
				superior = max(alturasmidi)
				alturaaux = note.Note()
				alturaaux.pitch.midi = superior
				nuevabajo = alturaaux.transpose(intervalo).pitch
				restr_bajo.append(nuevabajo.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitches = compas.notes[0].transpose(intervalo).pitches
			else: #si es una nota comun
				nuevabajo = compas.notes[0].transpose(intervalo).pitch
				restr_bajo.append(nuevabajo.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitch = nuevabajo
			compas.notes[0].color = 'blue'
	
	if len (bajo[-1].notes) > 1: #es decir si hay mas de una nota en el ultimo compas
		if bajo[-1].notes[-1].isChord:		
			alturasmidi = [a.midi for a in bajo[-1].notes[-1].pitches]
			superior = max(alturasmidi)
			alturaaux = note.Note()
			alturaaux.pitch.midi = superior
			nuevabajo = alturaaux.transpose(intervalo).pitch
			restr_bajo.append(nuevacont.pitchClass) #guardo la nota transportada a do
			bajo[-1].notes[-1].pitches = bajo[-1].notes[-1].transpose(intervalo).pitches
		else:
			nuevacont = bajo[-1].notes[-1].transpose(intervalo).pitch
			restr_bajo.append(nuevacont.pitchClass) #la ultima nota
		bajo[-1].notes[-1].color = 'blue'
		nbajo.append(0)
	veclargos = [nsoprano, ncontralto, ntenor, nbajo]
	escribir(veclargos, filelargos ) #aca escribo la matriz con los veclargos
	vecnotas = [restr_sop, restr_cont, restr_ten, restr_bajo]
	escribir(vecnotas, filenotas)	
	return [vecnotas, veclargos]


#la funcion restricciones modificada (usa escribir2 y cambia la forma de los archivos que escribe). No elijo filenames

def restricciones2(coral):
	original = coral
	tono = original.analyze('key')
	tonica = note.Note()
	tonica.pitch = tono.pitchFromDegree(1)
	do = note.Note('C')
	intervalo = interval.Interval(tonica, do)		
	soprano = original.parts[0].getElementsByClass(stream.Measure)
	contralto = original.parts[1].getElementsByClass(stream.Measure)
	tenor = original.parts[2].getElementsByClass(stream.Measure)
	bajo = original.parts[3].getElementsByClass(stream.Measure)
	nsoprano = []
	ncontralto = []
	ntenor = []
	nbajo = []		
	restr_sop = []
	restr_cont = []
	restr_ten = []
	restr_bajo = []
	for compas in soprano:
		if len(compas.notes) >0:
			nsoprano.append(len(compas.notes))			
			if compas.notes[0].isChord:
				alturasmidi = [a.midi for a in compas.notes[0].pitches]
				superior = max(alturasmidi)
				alturaaux = note.Note()
				alturaaux.pitch.midi = superior
				nuevasop = alturaaux.transpose(intervalo).pitch
				restr_sop.append(nuevasop.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitches = compas.notes[0].transpose(intervalo).pitches
			else: #si es una nota comun
				nuevasop = compas.notes[0].transpose(intervalo).pitch
				restr_sop.append(nuevasop.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitch = nuevasop
			compas.notes[0].color = 'blue' 
	if len (soprano[-1].notes) > 1: #es decir si hay mas de una nota en el ultimo compas
		if soprano[-1].notes[-1].isChord:		
			alturasmidi = [a.midi for a in soprano[-1].notes[-1].pitches]
			superior = max(alturasmidi)
			alturaaux = note.Note()
			alturaaux.pitch.midi = superior
			nuevasop = alturaaux.transpose(intervalo).pitch
			restr_sop.append(nuevasop.pitchClass) #guardo la nota transportada a do
			soprano[-1].notes[-1].pitches = soprano[-1].notes[-1].transpose(intervalo).pitches
		else:
			nuevasop = soprano[-1].notes[-1].transpose(intervalo).pitch
			restr_sop.append(nuevasop.pitchClass) #la ultima nota
		soprano[-1].notes[-1].color = 'blue' 
		nsoprano.append(0) #para que el script en R no falle
	
	for compas in contralto:
		if len(compas.notes) >0:
			ncontralto.append(len(compas.notes))
			if compas.notes[0].isChord:
				alturasmidi = [a.midi for a in compas.notes[0].pitches]
				superior = max(alturasmidi)
				alturaaux = note.Note()
				alturaaux.pitch.midi = superior
				nuevacont = alturaaux.transpose(intervalo).pitch
				restr_cont.append(nuevacont.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitches = compas.notes[0].transpose(intervalo).pitches
			else: #si es una nota comun
				nuevacont = compas.notes[0].transpose(intervalo).pitch
				restr_cont.append(nuevacont.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitch = nuevacont
			compas.notes[0].color = 'blue'
	
	if len (contralto[-1].notes) > 1: #es decir si hay mas de una nota en el ultimo compas
		if contralto[-1].notes[-1].isChord:		
			alturasmidi = [a.midi for a in contralto[-1].notes[-1].pitches]
			superior = max(alturasmidi)
			alturaaux = note.Note()
			alturaaux.pitch.midi = superior
			nuevacont = alturaaux.transpose(intervalo).pitch
			restr_cont.append(nuevacont.pitchClass) #guardo la nota transportada a do
			contralto[-1].notes[-1].pitches = contralto[-1].notes[-1].transpose(intervalo).pitches
		else:
			nuevacont = contralto[-1].notes[-1].transpose(intervalo).pitch
			restr_cont.append(nuevacont.pitchClass) #la ultima nota
		contralto[-1].notes[-1].color = 'blue'
		ncontralto.append(0)
	for compas in tenor:
		if len(compas.notes) >0:
			ntenor.append(len(compas.notes))
			if compas.notes[0].isChord:
				alturasmidi = [a.midi for a in compas.notes[0].pitches]
				superior = max(alturasmidi)
				alturaaux = note.Note()
				alturaaux.pitch.midi = superior
				nuevaten = alturaaux.transpose(intervalo).pitch
				restr_ten.append(nuevaten.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitches = compas.notes[0].transpose(intervalo).pitches
			else: #si es una nota comun
				nuevaten = compas.notes[0].transpose(intervalo).pitch
				restr_ten.append(nuevaten.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitch = nuevaten
			compas.notes[0].color = 'blue'
	
	if len (tenor[-1].notes) > 1: #es decir si hay mas de una nota en el ultimo compas
		if tenor[-1].notes[-1].isChord:		
			alturasmidi = [a.midi for a in tenor[-1].notes[-1].pitches]
			superior = max(alturasmidi)
			alturaaux = note.Note()
			alturaaux.pitch.midi = superior
			nuevaten = alturaaux.transpose(intervalo).pitch
			restr_ten.append(nuevacont.pitchClass) #guardo la nota transportada a do
			tenor[-1].notes[-1].pitches = tenor[-1].notes[-1].transpose(intervalo).pitches
		else:
			nuevaten = tenor[-1].notes[-1].transpose(intervalo).pitch
			restr_ten.append(nuevaten.pitchClass) #la ultima nota
		tenor[-1].notes[-1].color = 'blue'
		ntenor.append(0)
	for compas in bajo:
		if len(compas.notes) >0:
			nbajo.append(len(compas.notes))
			if compas.notes[0].isChord:
				alturasmidi = [a.midi for a in compas.notes[0].pitches]
				superior = max(alturasmidi)
				alturaaux = note.Note()
				alturaaux.pitch.midi = superior
				nuevabajo = alturaaux.transpose(intervalo).pitch
				restr_bajo.append(nuevabajo.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitches = compas.notes[0].transpose(intervalo).pitches
			else: #si es una nota comun
				nuevabajo = compas.notes[0].transpose(intervalo).pitch
				restr_bajo.append(nuevabajo.pitchClass) #guardo la nota transportada a do
				compas.notes[0].pitch = nuevabajo
			compas.notes[0].color = 'blue'
	
	if len (bajo[-1].notes) > 1: #es decir si hay mas de una nota en el ultimo compas
		if bajo[-1].notes[-1].isChord:		
			alturasmidi = [a.midi for a in bajo[-1].notes[-1].pitches]
			superior = max(alturasmidi)
			alturaaux = note.Note()
			alturaaux.pitch.midi = superior
			nuevabajo = alturaaux.transpose(intervalo).pitch
			restr_bajo.append(nuevacont.pitchClass) #guardo la nota transportada a do
			bajo[-1].notes[-1].pitches = bajo[-1].notes[-1].transpose(intervalo).pitches
		else:
			nuevacont = bajo[-1].notes[-1].transpose(intervalo).pitch
			restr_bajo.append(nuevacont.pitchClass) #la ultima nota
		bajo[-1].notes[-1].color = 'blue'
		nbajo.append(0)
	#genero 4 archivos de veclargos y vecnotas, con TODOS los veclargos y vecnotas para cada voz
	escribir2([nsoprano], 'veclargos_sop') #aca escribo los veclargos
	escribir2([ncontralto], 'veclargos_cont')
	escribir2([ntenor], 'veclargos_ten')
	escribir2([nbajo], 'veclargos_bajo')
	#vecnotas = [restr_sop, restr_cont, restr_ten, restr_bajo]
	escribir2([restr_sop], 'vecnotas_sop')
	escribir2([restr_cont], 'vecnotas_cont')
	escribir2([restr_ten], 'vecnotas_ten')
	escribir2([restr_bajo], 'vecnotas_bajo')	
	#return [vecnotas, veclargos] no devuelvo nada


#Agosto 2017: convierte la secuencia de 1s y 0s a objetos music21 con la estructura de compas indicada.

def armarmetrica(vectorgolpes, bpc, compas): #compas en formato 'num/den'
	salida = stream.Stream()
	comp = meter.TimeSignature(compas)
	compases = stream.Measure()
	ql = float(comp.numerator)*4/(comp.denominator *bpc) #el largo en quarterlength de los golpes
	compases.append(comp)
	duracion = 0
	indice = 0
	durac_compas = 0
	while vectorgolpes[indice] != 1: #en caso de que haya silencios al principio, asumo no duran mas de un compas
		duracion += ql
		indice +=1
	if indice!= 0:
		silencio = note.Rest()
		silencio.duration.quarterLength = duracion
		compases.append(silencio)
	duracion = ql
	for i in range(indice+1,len(vectorgolpes)):
		if i%bpc == 0: #i.e, si estoy empezando un nuevo compas
			notadummy = note.Note()
			notadummy.duration.quarterLength = duracion
			compases.append(notadummy) #agrego nota al compas
			duracion = ql
			salida.append(compases) #agrego compas a la parte
			compases = stream.Measure() #nuevo compas
			if vectorgolpes[i] == 1: #si hay ataque al principio del compas
				notadummy = note.Note()
			else:
				notadummy = note.Rest()
		else:
			if vectorgolpes[i] == 0:
				duracion +=ql
			else: #i.e, si es 1	
				if len(compases) == 0: #si estoy en la primer nota del compas, uso la notadummy definida arriba
					notadummy.duration.quarterLength = duracion
				else:
					notadummy = note.Note()
					notadummy.duration.quarterLength = duracion
				compases.append(notadummy)
				duracion = ql
	compases = stream.Measure()
	compases.append(note.Note())
	compases.append(note.Rest()) #ultima nota y silencios agregados a mano
	salida.append(compases)
	return salida


