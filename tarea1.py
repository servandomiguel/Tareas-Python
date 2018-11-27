#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT

def encuentra_palindromo(cadena):
	"""
			Funcion que encuentra el palindromo mas grande 
			dentro de una cadena.

			Devuelve una cadena con el palindromo

			La forma de utilizarse:
				encuentra_palindromo(cadena) donde:
					
					cadena debe ser una cadena 
					de caracteres
				 
	"""
	n=0
	m=0
	subcadena = ''
	palindromo = ''
	while n < len(cadena):
		while m <= len(cadena):
			subcadena = cadena[n:m]
			if subcadena == subcadena[::-1]:
				if len(subcadena) > len(palindromo):
					palindromo = subcadena
			m += 1
		n += 1
		m=n
	return palindromo


print '******************* 1 ****************'
print encuentra_palindromo('aleteetelxaxanxitaxlavxalaxtinaaxavnhgjghjghjaaleteetelaar')


def es_primo(numero):
	"""	
			Funcion que devuelve True en caso de que el argumento 
			sea un numero primo, False si el argumento no es un 
			numero primo 

			La forma de utilizarse:
					es_primo(numero) donde:

						numero debe ser un entero positivo 
			
	"""
	numeros = [2,3,4,5,6,7,8,9,10,11]
	if numero in numeros:
		numeros.remove(numero)
	for e in numeros:
		if numero%e == 0:
			return False
	return True
print '******************* 2 ****************'
print "El 2 es primo: " + str(es_primo(2))
print "El 3 es primo: " + str(es_primo(3))
print "El 4 es primo: " + str(es_primo(4))
print "El 5 es primo: " + str(es_primo(5))
print "El 17 es primo: " + str(es_primo(17))
print "El 18 es primo: " + str(es_primo(18))
print "El 19 es primo: " + str(es_primo(19))
print "El 929 es primo: " + str(es_primo(929))
print "El 930 es primo: " + str(es_primo(930))

lista = []
def n_primos(l,n):
	"""
			Funcion recursiva que genera una lista de 
			los primeros n numero primos, n no es 
			inclusivo

			Devuelve una lista con los numeros primos 
			que se encuentran desde 0 hasta n

			La forma de utilizarse:
				n_primos(l,n) donde:
					l es una lista vacia donde 
						se guardaran los numeros
					n es un entero que corresponde 
						al numero hasta el cual se 
						generara la lista
	"""
	
	if n == 2:
		return True
	if n_primos(l,n-1):
		l.append(n-1)
	return es_primo(n)

n_primos(lista,101)
print '******************* 3 ****************'
print lista
	 



