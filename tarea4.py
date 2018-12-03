#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
#XML - parser
import sys
import xml.etree.ElementTree as ET
from hashlib import md5, sha1
from datetime import datetime

class Host(object):

    def __init__(self, ip, estado, edo_puerto, es_honey, dn):
        self.ip = ip
        self.estado = estado
        self.edo_puerto  = edo_puerto
        self.es_honey = es_honey
        self.dn = dn


    def __str__(self):
        return '%s,%s,%s,%s,%s\n'%(self.ip, self.estado, self.edo_puerto, self.es_honey, self.dn)


def printError(msg, exit = False):
    sys.stderr.write('Error:\t%s\n' % msg)
    if exit:
        sys.exit(1)

def hasheando(filename):
    sh = sha1()
    md = md5()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            sh.update(b)
            md.update(b)
    return (sh.hexdigest() , md.hexdigest())

def strDate():
    return str(datetime.now())



def lee_xml(archivo_xml):
    h_apagados = 0 
    h_prendidos = 0
    h_p22 = 0
    h_p53 = 0
    h_p80 = 0
    h_p443 = 0
    h_apache = 0
    h_nginx = 0
    h_honey = 0
    h_otros = 0
    h_dn = 0
    edo = False
    edo_p = False
    es_h = False
    dn = ''
    ba = True
    bn = True
    bh = True
    lista_hosts = []

    with open(archivo_xml,'r') as fl:
        root = ET.fromstring(fl.read())

        #print "+++++++++++++++++++++++++++++++++++++"
        for host in root.findall('host'):
                es_h = False
                edo_p = False
                ba = True
                bn = True
                bh = True
                bo = True
                dn = ''
            #try:
                #print "---------------------------------------"
                if host.find('status').get('state') == 'up':
                    h_prendidos += 1
                    edo = True
                else: 
                    h_apagados += 1
                    edo = False

                hostnames = host.find('hostnames')
                if hostnames is not None:
                    for hostname in hostnames.findall('hostname'):
                        dn = hostname.get('name')
                        if '.' in dn:
                            h_dn += 1
                            break

                ports = host.find('ports')
                if ports is not None:
                    for port in ports.findall('port'):
                        if port.get('portid') == '22' and port.find('state').get('state') == 'open':
                            h_p22 += 1
                            edo_p = True
                        elif port.get('portid') == '53' and port.find('state').get('state') == 'open':
                            h_p53 += 1
                        elif port.get('portid') == '80' and port.find('state').get('state') == 'open':
                            h_p80 += 1
                        elif port.get('portid') == '443' and port.find('state').get('state') == 'open':
                            h_p443 += 1
                       
                        t1 = port.find('service').get('product')
                        if t1 is not None:
                            if 'dionaea' in t1.lower() and bh:
                                h_honey += 1
                                bh = False
                                es_h = True
                            elif 'apache' in t1.lower() and ba:
                                h_apache += 1
                                ba = False
                            elif 'nginx' in t1.lower()and bn:
                                h_nginx += 1
                                bn = False

                            else:
                                if bo:
                                    h_otros += 1
                                    bo = False


                lista_hosts.append(Host(host.find('address').get('addr'),  edo , edo_p , es_h , dn  ))
                #raw_input('..')
    return (h_prendidos,h_apagados,h_p22,h_p53,h_p80,h_p443,h_apache,h_nginx,h_honey,h_otros,h_dn,lista_hosts)

def escribeReporte(archivo_xml,reporte, elementos):
    cadenas = ['Hosts encendidos : ','Hosts apagados : ','Hosts p 22: ','Hosts p 53: ','Hosts p 80 : ','Hosts p 443: ','Apaches : ', 'Nginxs: ', 'Honeys: ', 'Otros : ', 'DomainNames: ']
    strdate = 'Fecha : ' +  strDate()
    sh, md = hasheando(archivo_xml)
    with open(reporte, 'w') as fl:
        print strdate 
        fl.write(strdate + '\n')
        print 'Sha1-> ' + sh
        fl.write('Sha1-> ' + sh + '\n')
        print 'MD5 -> ' + md
        fl.write('MD5 -> ' + md + '\n')
        for e in range(len(elementos)):
            print cadenas[e] + str(elementos[e])
            fl.write(cadenas[e] + str(elementos[e]) + '\n')

def escribeCSV(archivo, hosts):
    with open(archivo+'.csv','w') as fl:
        for host in hosts:
            fl.write(str(host) + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        printError('Indicar archivo a leer y archivo de reporte.', True)
    
    elementos = tuple(lee_xml(sys.argv[1]))
    escribeReporte(sys.argv[1], sys.argv[2], elementos[:-1] )
    escribeCSV(sys.argv[2], elementos[-1])


