#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT

from random import randint


def crear_password(tamm):
	"""
		Funcion que genera un password con las siguientes caracterisitcas:
			* Tamanio minimo de 15			
			* Un simbolo especia
			* Una letra mayuscula
			* Una letra minuscula
			* Un numero 
			* Los caracteres restantes se completan con una mezcla de 
				los anteriores

		La Funcion se llama de la siguiete forma 
			crear_password(un_numero_entero_mayor_a_14)
		
		Devuelve una cadena vacia si el argumento es menor a 15
		Devuelve una cadena con un password generado si el argumento es mayor a 14
	
	"""
	if 15 > tamm:
		print "El tamanio minimo es 15"
		return ''
	return generador_password(tamm)

def generador_password(tamm):
	"""
			Funcion recursiva que genera un password aleatorio 
			se recomienda no llamarla directanente, en su lugar 
			usar la funcion crear_password(tamm)

			Devuelve una cadena de caracteres que contiene un password

			Se llama de la siguiente forma:
				generador_password(num) donde:
						num debe ser > 14
	"""
	if tamm == 0:
		return chr(randint(33,122))
	elif tamm == 2:
		return chr(randint(33,47)) + generador_password(tamm-1)
	elif tamm == 5:
		return chr(randint(48,57)) + generador_password(tamm-1)
	elif tamm == 10:
		return chr(randint(65,90)) + generador_password(tamm-1)
	elif tamm == 13:
		return chr(randint(97,122)) + generador_password(tamm-1)
	else:
		return chr(randint(33,122)) + generador_password(tamm-1)

print 'Password generado : ' + crear_password(16)
	
	

		
