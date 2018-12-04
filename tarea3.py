#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
from itertools import permutations
import sys
def traerPalabras(archivo):
    with open(archivo, 'r') as fl:
        return [ linea.lower()[:-1]  for linea in fl.readlines() ]

def aMayusculas(palabra):
    m = 0
    n = 0
    lista_palabras = [palabra]
    while m < len(palabra):
        cadena = palabra
        n = m
        while n < len(palabra):
            if n == 0:
                cadena = cadena[:n+1].upper() + cadena[n+1:]
            else:
                cadena =  cadena[:n] + cadena[n].upper() + cadena[n+1:]
            n += 1
            lista_palabras.append(cadena)
        m +=1
    return lista_palabras

def aNumeros(lista_palabras):
    m = 0
    n = 0
    d = {'a':'4','A':'4','b':'8','B':'8','e':'3','E':'3','g':'6','G':'6','i':'1','I':'1',
            'o':'0','O':'0','q':'9','Q':'9','s':'5','S':'5','t':'7','T':'7'}
    for palabra in lista_palabras:
        cadena = palabra
        n = m
        while m < len(palabra):
        	cadena = palabra
        	n = m
        	while n < len(palabra):
        		n_cad = cadena
        		if n == 0:
        			cadena = d[cadena[:n+1]] + cadena[n+1:] if cadena[:n+1] in d.keys() else cadena
        		else:
        			cadena =  cadena[:n] + d[cadena[n]] + cadena[n+1:] if cadena[n] in d.keys() else cadena
        		n += 1
        		if n_cad != cadena and not cadena in lista_palabras:
        			lista_palabras.append(cadena)
        		
        	m +=1
    return lista_palabras

def aLetrasMinusculas(palabra):
	m = 0
	n = 0
	d = {'4':'a','8':'b','3':'e','6':'g','1':'i','0':'o','9':'q','5':'s','7':'t'}
	lista_palabras = []
	
	while m < len(palabra):
		cadena = palabra
		n = m
		while n < len(palabra):
			n_cad = cadena
			if n == 0:
				cadena = d[cadena[:n+1]] + cadena[n+1:] if cadena[:n+1] in d.keys() and cadena[:n+1].isdigit() else cadena
			else:
				cadena =  cadena[:n] + d[cadena[n]] + cadena[n+1:] if cadena[n] in d.keys() and cadena[n].isdigit() else cadena
			n += 1
			if n_cad != cadena and not cadena in lista_palabras:
				lista_palabras.append(cadena)
		m += 1
	return lista_palabras


def aLetrasMayusculas(palabra):
	m = 0
	n = 0
	d = {'4':'A','8':'B','3':'E','6':'G','1':'I','0':'O','9':'Q','5':'S','7':'T'}
	lista_palabras = []
	
	while m < len(palabra):
		cadena = palabra
		n = m
		while n < len(palabra):
			n_cad = cadena
			if n == 0:
				cadena = d[cadena[:n+1]] + cadena[n+1:] if cadena[:n+1] in d.keys() and cadena[:n+1].isdigit() else cadena
			else:
				cadena =  cadena[:n] + d[cadena[n]] + cadena[n+1:] if cadena[n] in d.keys() and cadena[n].isdigit() else cadena
			n += 1
			if n_cad != cadena and not cadena in lista_palabras:
				lista_palabras.append(cadena)
		m += 1
	return lista_palabras
	
def crearListas(archivo_entrada):
	lista_archivos = []
	for palabra in traerPalabras(archivo_entrada):
		lista_palabras = aNumeros(aMayusculas(palabra))
		lista_palabras.extend(aLetrasMinusculas(palabra))
		lista_palabras.extend(aLetrasMayusculas(palabra))
		
		archivo_salida = 'xxxyyzzz.'+palabra
		with open(archivo_salida, 'w') as fl:
			for p in lista_palabras:
				fl.write(p+'\n')
		lista_archivos.append(archivo_salida)
	return lista_archivos
	
def generarNumeros():
	return map((lambda x: str(x)) , range(1000))
	
def generarListaSimbolos():
	l1 = ['`','~','!','@','#','$','%','^','&','*','(',')','-','_','=','+','[','{',']','}','\\','|',';',':','\"','\'',',','<','.','>','?']
	lf = []
	lf.extend(l1)	
	
	for e1 in range(len(l1)):
		for e2 in range(len(l1)):
			lf.append(l1[e1]+l1[e2])
	
	# Si se desena generar mas combinaciones descomentar
	#for e1 in range(len(l1)):
	#	for e2 in range(len(l1)):
	#		for e3 in range(len(l1)):
	#			lf.append(l1[e1]+l1[e2]+l1[e3])
		
	return lf

def generarPasswords(archivos, numeros , simbolos , salida):
	with open(salida,'w') as fo:
		for archivo in archivos:
			with open(archivo, 'r') as fl1:
				for palabra in fl1.readlines():
					fo.write(palabra)
		
			combinaciones = permutations(archivos,2)
			for e in combinaciones:
				with open(e[0],'r') as f1, open(e[1],'r') as f2:
					for p1 in f1.readlines():
						for p2 in f2.readlines():
							for numero in numeros:
								fo.write(p1[:-1]+numero+p2[:-1]+'\n')
							for simbolo in simbolos:
								fo.write(p1[:-1]+simbolo+p2[:-1]+'\n')
			
			combinaciones = permutations(archivos,3)
			for e in combinaciones:
				with open(e[0],'r') as f1, open(e[1],'r') as f2, open(e[2],'r') as f3:
					for p1 in f1.readlines():
						for p2 in f2.readlines():
							for p3 in f3.readlines():
								for e1 in range(len(numeros)):
									for e2 in range(len(numeros)):
										fo.write(p1[:-1]+numeros[e1]+p2[:-1]+numeros[e2]+p3[:-1]+'\n')
								for e1 in range(len(simbolos)):
									for e2 in range(len(simbolos)):
										fo.write(p1[:-1]+simbolos[e1]+p2[:-1]+simbolos[e2]+p3[:-1]+'\n')
								for e1 in range(len(numeros)):
									for e2 in range(len(simbolos)):
										fo.write(p1[:-1]+numeros[e1]+p2[:-1]+simbolos[e2]+p3[:-1]+'\n')
										fo.write(p1[:-1]+simbolos[e2]+p2[:-1]+numeros[e1]+p3[:-1]+'\n')
		
if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'Error los parametros no son correctos!'
		print '\n Modo de uso'
		print '\n\tpython tarea3.py archivo_de_entrada archivo_de_resultados'		
	#print traerPalabras('password.txt')
	#print aMayusculas('bruno')
	#print aNumeros(['serpiente'])
	#print aLetrasMinusculas('j0rg3')
	#print aLetrasMayusculas('j0rg3')
	#print generarListaSimbolos()
	archivos = crearListas(sys.argv[1])
	numeros = generarNumeros()
	simbolos = generarListaSimbolos()
	
	
	generarPasswords(archivos ,numeros , simbolos , sys.argv[2])
	
	
    
    
    
