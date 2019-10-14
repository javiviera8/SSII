#!/usr/bin/python
# vim: set fileencoding=<encoding name> : ^[ \t\f]#.?coding[:=][ \t]*([-_.a-zA-Z0-9]+)
#Instalar sudo apt-get install python-pip
#Instalar sudo apt-get install pyhton-pandas
#Instalar sudo apt-get install python-matplotlib

import hashlib
import configparser
import os
import shutil
import time
import matplotlib.pyplot as plt
import pandas as pd
import datetime


###FUNCIONANDO###
#Funcion que lee el archivo de configuracion.
def leeArchivoConfig():
    rutaArchivoConfig = os.getcwd() + str('/config.ini')
    config = configparser.ConfigParser()
    config.read('config.ini')
    algoritmo = config['PARAM']['MODE']
    tiempo = config['PARAM']['TIME']
    rutaDirectorio = config['RUTAS']['DIR']
    rutaFicheroHashesOld = config['RUTAS']['HASHOLD']
    rutaFicheroHashesNew = config['RUTAS']['HASHNEW']
    rutaFicheroIncidencias = config['RUTAS']['INCD']
    rutaFicheroIndicadores = config['RUTAS']['INDIC']
    rutaFicheroHorasEjecucion = config['RUTAS']['HEJEC']
    listaArchivos = []
    for i in config['ARCHIVOS']:
        listaArchivos.append(str(config['ARCHIVOS'][i.upper()]))
    return algoritmo,tiempo,rutaDirectorio,rutaFicheroHashesOld,rutaFicheroHashesNew,rutaFicheroIncidencias,rutaFicheroIndicadores,rutaFicheroHorasEjecucion,listaArchivos
    
algoritmo,tiempo,rutaDirectorio,rutaFicheroHashesOld,rutaFicheroHashesNew,rutaFicheroIncidencias,rutaFicheroIndicadores,rutaFicheroHorasEjecucion,listaArchivos = leeArchivoConfig()

###FUNCIONANDO###
#Funcion que genera la ruta de los archivos que se encuentran
#dentro del directorio especificado por parametros.
def calculaRutaArchivo(rutaDirectorio):
    listaRes = []
    for i in listaArchivos:
        listaRes.append(str(rutaDirectorio + i))
    return listaRes

###FUNCIONANDO###
#Funcion que calcula los hashes de cada uno de los archivos
#contenidos en el directorio especificado por parametros
#con el algoritmo que le digamos por parametros (sha1,sha256...).
def calculaHashesArchivos(algoritmo, rutaDirectorio):
    listaRes = []
    listaArchivos = calculaRutaArchivo(rutaDirectorio)
    for i in listaArchivos:
        hasher = hashlib.new(algoritmo)
        file = open(i, "r")
        contents = file.read()
        hasher.update(contents)
        listaRes.append(hasher.hexdigest())
    return listaRes

###FUNCIONANDO###
#Funcion que escribe en un fichero de texto los hashes de los archivos
#contenidos en el directorio especificado por parametros haciendo uso del
#algoritmo pasado por paramertros.
def escribeFicheroHashesNew(algoritmo, rutaDirectorio, rutaFicheroHashesNew):
    listaHashes = calculaHashesArchivos(algoritmo,rutaDirectorio)
    file = open(rutaFicheroHashesNew, "w")
    for i in listaHashes:
        file.write(i + str("\n"))
    file.close()

###FUNCIONANDO###
#Funcion que los hashes escritos en el fichero HashesNew 
#al fichero HashesOld.
def copiaNewToOld(rutaFicheroHashesNew, rutaFicheroHashesOld):
    ruta = os.getcwd() + os.sep
    origen = rutaFicheroHashesNew
    destino = rutaFicheroHashesOld
    if os.path.exists(origen):
        with open(origen,'rb') as forigen:
            with open(destino, 'wb') as fdestino:
                shutil.copyfileobj(forigen, fdestino)
                
###FUNCIONANDO###
#Funcion que calcula el hash code del archivo que se especifica 
#por la ruta del parametro de entrada.
def calculaHash(algoritmo,ruta):
    hasher = hashlib.new(algoritmo)
    file = open(ruta, "r")
    contents = file.read()
    hasher.update(contents)
    return hasher.hexdigest()

###FUNCIONANDO###
#Funcion que al pasarle la ruta de mabos ficheros de hashes, compara
# si ambos son iguales o no
def comparaFicherosHash(hashCodeNew,hashCodeOld,rutaFicheroHashesNew,rutaFicheroHashesOld,numeroArchivosCorruptos):
    cont = 0
    fNew = open(rutaFicheroHashesNew,"r")
    fOld = open(rutaFicheroHashesOld,"r")
    if(hashCodeNew!=hashCodeOld):
        fIncidencias = open(rutaFicheroIncidencias, "a")
        listaIncidencias = []
        for iNew, iOld in zip(fNew,fOld):
            if(iNew!=iOld):
                nombreArchivo = listaArchivos[cont]
                #linea = "### La linea " + str(cont) + " del fichero HashesNew.txt [" + iNew + "] ha sido modificada respecto al fichero HashesOld.txt [" + iOld + "] ----- " + str(time.strftime("%c")) + " ###\n" 
                linea = "### Se ha modificado " + nombreArchivo + "-----"+ str(time.strftime("%c")) + " ###\n"
                fIncidencias.write(linea)
                numeroArchivosCorruptos = numeroArchivosCorruptos + 1
                print linea
            cont = cont + 1
        fIncidencias.close()
    else:
        print "Los ficheros HashesOld y HashesNew son iguales!"
    return numeroArchivosCorruptos

###FUNCIONANDO###
#Funcion que escribe que genera un fichero con el tanto porciento
#correspondiente con la integridad de la informacion de nuestro
#directorio.
def escribeFicheroIndicadores(hashCodeNew,hashCodeOld,rutaFicheroHashesNew,rutaFicheroHashesOld):
    total = 0.0
    incidencias = 0.0
    fNew = open(rutaFicheroHashesNew,"r")
    fOld = open(rutaFicheroHashesOld,"r")
    fIndicadores = open(rutaFicheroIndicadores, "a")
    if(hashCodeNew!=hashCodeOld):
        for iNew, iOld in zip(fNew, fOld):
            if(iNew!=iOld):
                incidencias = incidencias + 1.0
                total = total + 1.0
            else:
                total = total + 1.0
        #print "### Integridad de la informacion: " + str(100 - ((incidencias/(total))*100)) + "% ###\n"
        linea = "### Integridad de la informacion: " + str(100 - ((incidencias/(total))*100)) + "% ###\n"
        fIndicadores.write(linea)
    else:
        total = total + 1.0
        #print "### Integridad de la informacion: " + str(total*100) + "% ###\n"
        linea = "### Integridad de la informacion: " + str(total*100) + "% ###\n"
        fIndicadores.write(linea)
    fIndicadores.close()
    
##TO DO##
#
def generaGrafica(listaArchivos, numeroArchivosCorruptos):
    nombres= ('Archivos','Archivos Corruptos')
    cantidad= (len(listaArchivos)-numeroArchivosCorruptos,numeroArchivosCorruptos)
    colores= ('green','red')
    valores = (0, 0.1)
    plt.rcParams['toolbar']='None'
    plt.pie(cantidad, colors=colores, autopct='%1.1f%%', explode=valores, startangle=90)
    plt.axis('equal')
    plt.title('Grafica de archivos corruptos -- ' + str(datetime.datetime.now()) )
    plt.legend(labels=nombres)
    plt.savefig("Grafica.png")
    
def horasDeEjecucion():
    now=datetime.datetime.now()
    new_file = open(rutaFicheroHorasEjecucion, "a")
    new_file.write("Hora : " + str(now) + "\n")
    new_file.close()

#Funcion utilizada como metodo main
def main():
    
    numeroArchivosCorruptos = 0
    
    horasDeEjecucion() 
    
    print listaArchivos
    
    listaRutaArchivosRes = calculaRutaArchivo(rutaDirectorio)
    print listaRutaArchivosRes
    
    listaHashesRes = calculaHashesArchivos(algoritmo,rutaDirectorio)
    print listaHashesRes
    
    copiaNewToOld(rutaFicheroHashesNew,rutaFicheroHashesOld)
    print 'Fichero hashes_new copiado con exito!'
    
    escribeFicheroHashesNew(algoritmo,rutaDirectorio,rutaFicheroHashesNew)
    print 'Fichero de hashes_new escrito con exito!'
    
    print 'HashCode ficheroHashesNew :' + calculaHash(algoritmo,rutaFicheroHashesNew)
    print 'HashCode ficheroHashesOld :' + calculaHash(algoritmo,rutaFicheroHashesOld)
    
    comparaFicherosHash(calculaHash(algoritmo,rutaFicheroHashesNew),calculaHash(algoritmo,rutaFicheroHashesOld),rutaFicheroHashesNew,rutaFicheroHashesOld,numeroArchivosCorruptos)
    
    escribeFicheroIndicadores(calculaHash(algoritmo,rutaFicheroHashesNew),calculaHash(algoritmo,rutaFicheroHashesOld),rutaFicheroHashesNew,rutaFicheroHashesOld)
    
    #numeroArchivosCorruptos = comparaFicherosHash(calculaHash(algoritmo,rutaFicheroHashesNew),calculaHash(algoritmo,rutaFicheroHashesOld),rutaFicheroHashesNew,rutaFicheroHashesOld,numeroArchivosCorruptos)

    generaGrafica(listaArchivos, numeroArchivosCorruptos)
    
    return 0

#Invocacion a la funcion main
main()
