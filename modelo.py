#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Title         : modelo.py
# Description   : Modelo del programa
# Author        : Julio Domingo Jiménez Ledesma
# Author        : Rafael Carlos Méndez Rodríguez
# Date          : 30-05-2018
# Version       : 1.0.0
# Usage         : import modelo o from modelo import ...
# Notes         : 


from __future__ import print_function


DEBUG = True

ESPERA = 1                                                                                                  # Tiempo de espera para que el padre compruebe la finalización de sus hijos

import os                                                                                                   # Funcionalidades varias del sistema operativo
import random                                                                                               # Generación de números aleatorios

from threading import Thread                                                                                # Capacidades multihilo
from time import sleep                                                                                      # Pausas

from rdflib import Graph                                                                                    # Grafos


class Element():                                                                                            # Representacion de un nodo en el grafo
    def __init__(self, nombre, duracion):                                                                   # Constructor de la clase
        self._nombre = nombre                                                                               # Inicialización de variables

        self._duracion = duracion

        self._padres = []

        self._conexiones = []


    def conexiones(self, conexion = None, multiples = False):                                               # Método "sobrecargado":
        if conexion != None:                                                                                #     Modificador de la variable
            if multiples == True:                                                                           #     Modificador múltiple
                self._conexiones = conexion

            else:                                                                                           #     Modificador simple
                self._conexiones.append(conexion)

        return self._conexiones                                                                             #     Observador de la variable


    def duracion(self, duracion = None):                                                                    # Método "sobrecargado":
        if duracion != None:                                                                                #     Modificador de la variable
            self._duracion = duracion

        return self._duracion                                                                               #     Observador de la variable


    def nombre(self, nombre = None):                                                                        # Método "sobrecargado":
        if nombre != None:                                                                                  #     Modificador de la variable
            self._nombre = nombre

        return self._nombre                                                                                 #     Observador de la variable


    def padres(self, padre = None, multiples = False):                                                      # Método "sobrecargado":
        if padre != None:                                                                                   #     Modificador de la variable
            if multiples == True:                                                                           #     Modificador múltiple
                self._padres = padre

            else:                                                                                           #     Modificador simple
                self._padres.append(padre)

        return self._padres                                                                                 #     Observador de la variable


class ventana_modelo():                                                                                     # Parte del modelo de la ventana
    def calcular(self, hilos):                                                                              # Cálculo de soluciones
        hijos = list()

        self.__soluciones = [[] for i in range(hilos)]                                                      # Inicialización del vector de soluciones

        nodos_padres = self.padres(self._datos)                                                             # Precarga del cálculo de los nodos padres (posibles nodos iniciales)

        for i in range(hilos):
            if DEBUG:
                print('Padre #', os.getpid(), "\tPreparando hijo ", i, sep = '')

            #Declarando los hijos. Ejecutarán ventana_modelo.calcular_hijos
            hijos.append(Thread(target = ventana_modelo.calcular_hijos, args = (self, i, nodos_padres,)))

            if DEBUG:
                print('Padre #', os.getpid(), "\tArrancando hijo ", i, sep = '')

            hijos[i].start()

        while hijos:                                                                                        # Mientras el vector tenga hijos
            for hijo in hijos:                                                                              # Para cada hijo del vector
                if not hijo.is_alive():                                                                     # Comprobación de si el hijo ha finalizado
                    hijo.join()                                                                             # Se recupera el proceso y se saca del vector
                    hijos.remove(hijo)

                    del(hijo)

            if DEBUG == True:
                print('Padre #', os.getpid(), "\tEsperando a que los procesos hijos hagan su trabajo", sep = '')

            sleep(ESPERA)                                                                                       # Para no saturar, el padre queda en espera durante "ESPERA" segundos

        #Recorriendo el vector con las soluciones dadas por los hijos (recorriendolo por ids en vez de por elementos)
        for i in range(len(self.__soluciones)):
            if DEBUG == True:
                print('Padre #', os.getpid(), "\tEl hijo ", i, ' ha aportado la solución: ', self.__soluciones[i], sep = '')


    def calcular_hijos(self, id_hijo, nodos_padres):                                                        # Cálculo de cada solución (ejecutada por cada hijo)
        if DEBUG:
            print('Hijo  #', id_hijo, "\tHe sido llamado", sep = '')

        prob_heuristica = random.randint(0, 100)                                                            # Probabilidad de utilizar la heurística
        #La heuristica evitará que todos los hijos converjan al mismo resultado (puede ser un óptimo local)

        #Descomponineod la lista nodos_padres en dos listas separadas
        padres, duraciones = zip(*nodos_padres)

        longitud_datos = len(self._datos)                                                                   # Precarga de la longitud del camino

        ''' Se establece un nodo inicial en función del la probabilidad de emplear la heurística:
                Si no se emplea, se elige un padre aleatoriamente
                Si sí, se elige al mejor en función de la duración de los mismos
        '''
        self.__soluciones[id_hijo].append( \
            random.choice(padres) \
            if random.randint(0, 100) < prob_heuristica \
            else padres[duraciones.index(min(duraciones))] \
        )
        
        while len(self.__soluciones[id_hijo]) < longitud_datos:                                             # Mientras que no hayamos explorado el grafo completo -> Mientras no queden máquinas por las que pasar
            hd = self._datos[self.__soluciones[id_hijo][len(self.__soluciones[id_hijo]) - 1]].conexiones()  # Lista de tuplas: (hijo, duracion)

            hijos, duraciones = zip(*hd)                                                                    # "Desempaquetado" en dos listas

            ''' Se establece un nodo siguiente en función del la probabilidad de emplear la heurística:
                    Si no se emplea, se elige un hijo aleatoriamente
                    Si sí, se elige al mejor en función de la duración de los mismos
            '''
            self.__soluciones[id_hijo].append( \
                random.choice(hijos) \
                if random.randint(0, 100) < prob_heuristica \
                else hijos[duraciones.index(min(duraciones))] \
            )


    @staticmethod                                                                                           # Método estático
    def convertir_conexiones_a_ids(elementos, conexiones):                                                  # Conversor de nombres a ids aplicado a conexiones
        res = []

        for conexion in conexiones:
            id_conexion = -1

            for id_elemento in range(len(elementos)):
                if elementos[id_elemento].nombre() == conexion[0]:
                    id_conexion = id_elemento

                    break

            res.append((id_conexion, conexion[1]))

        return res


    @staticmethod                                                                                           # Método estático
    def convertir_padres_a_ids(elementos, padres):                                                          # Conversor de nombres a ids aplicado a padres
        res = []

        for padre in padres:
            id_padre = -1

            for id_elemento in range(len(elementos)):
                if elementos[id_elemento].nombre() == padre:
                    id_padre = id_elemento

                    break

            res.append(id_padre)

        return res


    @staticmethod                                                                                           # Método estático
    def interpretar(grafo):                                                                                 # Interpreta un grafo dado: extrae la información necesaria para su posterior uso
        if DEBUG:
            print('Listando datos antes de ser almacenados en memoria...')

        elementos = []

        #Extrayendo máquinas del grafo
        query = '''
                    PREFIX    rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns>
                    PREFIX    maquina:  <http://www.factory.fake/maquina/>

                    SELECT    ?nombre ?duracion

                    WHERE {
                        ?maquina    rdf:type            maquina:maquina        .
                        ?maquina    maquina:nombre      ?nombre                .
                        ?maquina    maquina:duracion    ?duracion              .
                        }

                    # ORDER BY ?name
                '''

        resultado = grafo.query(query)

        #Para cada máquina...
        for fila in resultado:
            if DEBUG:
                print(fila.nombre, 'es una máquina con duración', fila.duracion)

            #Almacenando la máquina como un Element
            elemento = Element(fila.nombre, fila.duracion)

            #Buscando padres de la máquina...
            query = '''
                        PREFIX    maquina:  <http://www.factory.fake/maquina/>

                        SELECT    ?nombre_padre

                        WHERE {
                            ?maquina    maquina:nombre      "%s"              .
                            ?maquina    maquina:padre       ?padre            .
                            ?padre      maquina:nombre      ?nombre_padre     .
                            }
                    '''

            subresultado = grafo.query(query % fila.nombre)

            #Recorriendo la lista de padres
            for subfila in subresultado:
                if DEBUG:
                    print("\tPadre de ", elemento.nombre(), ': ', subfila.nombre_padre, sep = '')

                #Almancenando el nombre del padre de la máquina en el Element.
                elemento.padres(subfila.nombre_padre)

            #Buscando las conexiones de la máquina
            query = '''
                        PREFIX    maquina:  <http://www.factory.fake/maquina/>
                        PREFIX    conexion: <http://www.factory.fake/conexion/>

                        SELECT    ?nombre_siguiente ?duracion

                        WHERE {
                            ?maquina    maquina:nombre      "%s"              .
                            ?conexion   conexion:precedente ?maquina          .
                            ?conexion   conexion:siguiente  ?siguiente        .
                            ?conexion   conexion:duracion   ?duracion         .
                            ?siguiente  maquina:nombre      ?nombre_siguiente .
                            }
                    '''

            subresultado = grafo.query(query % fila.nombre)

            #Recorriendo la lista de conexiones
            for subfila in subresultado:
                if DEBUG:
                    print("\tConexión de ", elemento.nombre(), ': ', subfila.nombre_siguiente, ', ', subfila.duracion, sep = '')

                #Almacenando las conexiones en el Element
                elemento.conexiones((subfila.nombre_siguiente, int(subfila.duracion)))

            #Almacenando el Element elemento en la lista elementos -> Lista manejada
            elementos.append(elemento)

        if DEBUG:
            print()
            print()

        #Recorriendo la lista elementos para buscar las posiciones que ocupan en la lista
        for elemento in elementos:
            padres = elemento.padres()  #Obteniendo padres

            conexiones = elemento.conexiones()  #Obteniendo conexiones

            if padres != []:
                elemento.padres(ventana_modelo.convertir_padres_a_ids(elementos, padres), True)

            if conexiones != []:
                elemento.conexiones(ventana_modelo.convertir_conexiones_a_ids(elementos, conexiones), True)

        if DEBUG:
            print('Listando datos después de ser almacenados en memoria...')

            for i in range(len(elementos)):
                print(elementos[i].nombre(), 'es una máquina con duración', elementos[i].duracion())

                for j in elementos[i].padres():
                    print("\tPadre de ", elementos[i].nombre(), ': ', elementos[j].nombre(), sep = '')

                for (j, duracion) in elementos[i].conexiones():
                    print("\tConexión de ", elementos[i].nombre(), ': ', elementos[j].nombre(), ', ', duracion, sep = '')

            print()
            print()

        return elementos


    @staticmethod                                                                                           # Método estático
    def procesar(texto):                                                                                    # Procesa un texto: convierte un texto en formato NTriples a grafo
        grafo = Graph()

        try:
            grafo.parse(data = texto, format = 'n3')

        except:
            res = None

        else:
            res = grafo

        finally:
            return res


    @staticmethod                                                                                           # Método estático
    def padres(datos):                                                                                      # Devuelve una lista con las ids de los nodos padres y sus respectivas duraciones
        res = []

        for i in range(len(datos)):
            if datos[i].padres() == []:
                res.append((i, datos[i].duracion()))

        return res


