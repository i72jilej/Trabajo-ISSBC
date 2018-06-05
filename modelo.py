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


DEBUG       = True
DEBUG_HIJOS = False

ESPERA = 1                                                                                                              # Tiempo de espera para que el padre compruebe la finalización de sus hijos

import os                                                                                                               # Funcionalidades varias del sistema operativo
import random                                                                                                           # Generación de números aleatorios

if DEBUG:
    import sys                                                                                                          # Funcionalidades varias del sistema

from threading import Thread                                                                                            # Capacidades multihilo
from time import sleep                                                                                                  # Pausas

from rdflib import Graph                                                                                                # Grafos


class Element():                                                                                                        # Representacion de un nodo en el grafo
    def __init__(self, id_elemento, nombre, duracion):                                                                  # Constructor de la clase
        self._id_elemento = id_elemento                                                                                 # Inicialización de variables

        self._nombre = nombre

        self._duracion = duracion

        self._padres = []

        self._conexiones = []


    def conexiones(self, conexion = None, multiples = False):                                                           # Método "sobrecargado":
        if conexion != None:                                                                                            #     Modificador de la variable
            if multiples == True:                                                                                       #     Modificador múltiple
                self._conexiones = conexion

            else:                                                                                                       #     Modificador simple
                self._conexiones.append(conexion)

        return self._conexiones                                                                                         #     Observador de la variable


    def duracion(self, duracion = None):                                                                                # Método "sobrecargado":
        if duracion != None:                                                                                            #     Modificador de la variable
            self._duracion = duracion

        return self._duracion                                                                                           #     Observador de la variable


    def id_elemento(self, id_elemento = None):                                                                          # Método "sobrecargado":
        if id_elemento != None:                                                                                         #     Modificador de la variable
            self._id_elemento = id_elemento

        return self._id_elemento                                                                                        #     Observador de la variable


    def nombre(self, nombre = None):                                                                                    # Método "sobrecargado":
        if nombre != None:                                                                                              #     Modificador de la variable
            self._nombre = nombre

        return self._nombre                                                                                             #     Observador de la variable


    def padres(self, padre = None, multiples = False):                                                                  # Método "sobrecargado":
        if padre != None:                                                                                               #     Modificador de la variable
            if multiples == True:                                                                                       #     Modificador múltiple
                self._padres = padre

            else:                                                                                                       #     Modificador simple
                self._padres.append(padre)

        return self._padres                                                                                             #     Observador de la variable


class solucion():                                                                                                       # Representación de una solución
    def __init__(self):                                                                                                 # Constructor de la clase
        self._camino = []                                                                                               # Inicialización de variables
        self._duracion = 0


    def anyadir(self, nodo):                                                                                            # Añade un nodo a la solución, siempre que éste no esté ya en ella
        try:
            self._camino.index(nodo)                                                                                    # Comprobación de que no esté ya añadido

        except ValueError:                                                                                              # En caso de no estarlo:
            self.__duracion(nodo)                                                                                       #     Se recalcula la duración de la solución

            self._camino.append(nodo)                                                                                   #     Y se añade el nodo

            res = True                                                                                                  #     Se prepara el "informe"

        else:                                                                                                           # En caso de estar repetido:
            res = False                                                                                                 #     Se prepara el "informe"

        finally:
            return res                                                                                                  # Se devuelve el informe del éxito (o no) del añadido


    def camino(self):                                                                                                   # Observador de la variable
        return self._camino                                                                                             # Se entiende que un camino no se modificará (a excepción de añadir nuevos nodos al mismo)


    def __duracion(self, nodo):                                                                                         # Método interno para el recálculo de la duración de la solución
        if self._camino != []:                                                                                          # Si existe un camino
            for conexion in self._camino[len(self._camino) - 1].conexiones():                                           #     Se calcula la duración de la conexión entre el útimo nodo del mismo y el que se añadirá
                if conexion['objeto'] == nodo:
                    duracion_conexion = conexion['duracion']

                    break

        else:                                                                                                           # Si no:
            duracion_conexion = 0                                                                                       #     La duración es cero


        self._duracion += duracion_conexion + int(nodo.duracion())                                                      # La duración será la que actualmente haya más la duración de la conexión más la duración del nodo que se añadirá


    def duracion(self):                                                                                                 # Observador de la variable
        return self._duracion


class ventana_modelo():                                                                                                 # Parte del modelo de la ventana
    def calcular(self, hilos):                                                                                          # Cálculo de soluciones
        if DEBUG_HIJOS == True:
            hilos = 1

        hijos = list()

        self.__soluciones = [solucion() for i in range(hilos)]                                                          # Inicialización del vector de soluciones

        nodos_iniciales = self.iniciales(self._datos)                                                                   # Precáculo de los nodos iniciales

        for i in range(hilos):
            if DEBUG:
                print('Padre #', os.getpid(), "\tPreparando hijo ", i, sep = '')

            hijos.append(Thread(target = ventana_modelo.calcular_hijos, args = (self, i, nodos_iniciales,)))            # Declarando los hijos; ejecutarán ventana_modelo.calcular_hijos

            if DEBUG:
                print('Padre #', os.getpid(), "\tArrancando hijo ", i, sep = '')

            hijos[i].start()

        while hijos:                                                                                                    # Mientras el vector tenga hijos
            for hijo in hijos:                                                                                          # Para cada hijo del vector
                if not hijo.is_alive():                                                                                 # Comprobación de si el hijo ha finalizado
                    hijo.join()                                                                                         # Se recupera el proceso y se saca del vector
                    hijos.remove(hijo)

                    del(hijo)

            if DEBUG == True:
                print('Padre #', os.getpid(), "\tEsperando a que los procesos hijos hagan su trabajo", sep = '')

            sleep(ESPERA)                                                                                               # Para no saturar, el padre queda en espera durante "ESPERA" segundos

        self.__soluciones = self.podar(self.__soluciones)                                                               # Primera "poda"

        for una_solucion in self.__soluciones:                                                                          # Recorriendo la lista con las soluciones dadas por los hijos
                if DEBUG == True:
                    if sys.version_info[0] >= 3:
                        print('Padre #', os.getpid(), "\tPosible solución: ", [str(nodo.nombre()) for nodo in una_solucion.camino()], sep = '')

                    else:
                        print('Padre #', os.getpid(), "\tEl hijo ", i, ' ha aportado la solución: ', [nodo.nombre().toPython() for nodo in una_solucion.camino()], sep = '')


    def calcular_hijos(self, id_hijo, nodos_iniciales):                                                                 # Cálculo de cada solución (ejecutada por cada hijo)
        if DEBUG:
            print('Hijo  #', id_hijo, "\tHe sido llamado", sep = '')

        prob_heuristica = random.randint(0, 100)                                                                        # Probabilidad de utilizar la heurística
                                                                                                                        # La heuristica evitará que todos los hijos converjan al mismo resultado (puede ser un óptimo local)
        longitud_datos = len(self._datos)                                                                               # Precarga de la longitud del camino

        nodo_elegido = self.elegir(nodos_iniciales, prob_heuristica)

        self.__soluciones[id_hijo].anyadir(nodo_elegido)                                                                # Se añade un nodo inicial en función del la probabilidad de emplear la heurística

        if DEBUG:
            print('Hijo  #', id_hijo, "\tAñadido al camino el nodo", nodo_elegido.nombre())

        while len(self.__soluciones[id_hijo].camino()) < longitud_datos:                                                # Mientras queden máquinas por las que pasar
            if DEBUG:
                print('Hijo  #', id_hijo, "\tEl tamaño del árbol es de ", longitud_datos, ' nodos', sep = '')
                print('Hijo  #', id_hijo, "\tEl tamaño del camino es de ", len(self.__soluciones[id_hijo].camino()), ' nodos', sep = '')


            conexiones = self.__soluciones[id_hijo].camino()[len(self.__soluciones[id_hijo].camino()) - 1].conexiones() # Lista de tuplas: (hijo, duracion)

            nodos_conexiones = [conexion['objeto'] for conexion in conexiones]                                          # "Desempaquetado" en dos listas

            nodo_elegido = self.elegir(nodos_conexiones, prob_heuristica)

            if DEBUG:
                print('Hijo  #', id_hijo, "\tIntentando añadir al camino el nodo ", nodo_elegido.nombre(), sep = '')

            valido = self.__soluciones[id_hijo].anyadir(nodo_elegido)

            while not valido:
                if DEBUG:
                    print('Hijo  #', id_hijo, "\tNo es posible", sep = '')

                nodos_conexiones.remove(nodo_elegido)

                if nodos_conexiones != []:
                    nodo_elegido = self.elegir(nodos_conexiones, prob_heuristica)

                    if DEBUG:
                        print('Hijo  #', id_hijo, "\tIntentando añadir al camino el nodo ", nodo_elegido.nombre(), sep = '')

                    valido = self.__soluciones[id_hijo].anyadir(nodo_elegido)                                           # Se añade un nodo siguiente en función del la probabilidad de emplear la heurística

                else:
                    self.__soluciones[id_hijo] = solucion()

                    return


    @staticmethod                                                                                                       # Método estático
    def convertir_conexiones_a_elementos(elementos, conexiones):                                                        # Conversor de nombres a ids aplicado a conexiones
        res = []

        for conexion in conexiones:
            for id_elemento in range(len(elementos)):
                if elementos[id_elemento].nombre() == conexion[0]:
                    objeto_conexion = {'objeto': elementos[id_elemento], 'duracion': conexion[1]}

                    break

            res.append(objeto_conexion)

        return res


    @staticmethod                                                                                                       # Método estático
    def convertir_padres_a_elementos(elementos, padres):                                                                # Conversor de nombres a ids aplicado a padres
        res = []

        for padre in padres:
            for id_elemento in range(len(elementos)):
                if elementos[id_elemento].nombre() == padre:
                    objeto_padre = elementos[id_elemento]

                    break

            res.append(objeto_padre)

        return res


    @staticmethod
    def elegir(nodos, prob_heuristica):                                                                                 # Se elige un nodo en función del la probabilidad de emplear la heurística
        ''' Se elige un nodo en función del la probabilidad de emplear la heurística:
                Si no se emplea, se elige un hijo aleatoriamente
                Si sí, se elige al mejor en función de la duración de los mismos
        '''

        duraciones = [nodo.duracion() for nodo in nodos]                                                                # "Desempaquetado" en dos listas
        return \
            random.choice(nodos) \
            if random.randint(0, 100) < prob_heuristica \
            else nodos[duraciones.index(min(duraciones))]


    @staticmethod                                                                                                       # Método estático
    def iniciales(datos):                                                                                               # Devuelve una lista con las ids de los nodos padres y sus respectivas duraciones
        res = []

        for nodo in datos:
            if nodo.padres() == []:
                res.append(nodo)

        return res


    @staticmethod                                                                                                       # Método estático
    def interpretar(grafo):                                                                                             # Interpreta un grafo dado: extrae la información necesaria para su posterior uso
        if DEBUG:
            print('Listando datos antes de ser almacenados en memoria...')

        elementos = []
                                                                                                                        # Extrayendo máquinas del grafo
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

        for fila in resultado:                                                                                          # Para cada máquina...
            if DEBUG:
                print(fila.nombre, 'es una máquina con duración', fila.duracion)

            elemento = Element(len(elementos), fila.nombre, fila.duracion)                                              # Almacenando la máquina como un Element
                                                                                                                        # Buscando padres de la máquina...
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

            for subfila in subresultado:                                                                                # Recorriendo la lista de padres
                if DEBUG:
                    print("\tPadre:", subfila.nombre_padre)

                elemento.padres(subfila.nombre_padre)                                                                   # Almancenando el nombre del padre de la máquina en el Element
                                                                                                                        # Buscando las conexiones de la máquina
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

            for subfila in subresultado:                                                                                # Recorriendo la lista de conexiones
                if DEBUG:
                    print("\tConexión: ", subfila.nombre_siguiente, ', ', subfila.duracion, sep = '')

                elemento.conexiones((subfila.nombre_siguiente, int(subfila.duracion)))                                  # Almacenando las conexiones en el Element

            elementos.append(elemento)                                                                                  # Almacenando el Element elemento en la lista elementos -> Lista manejada

        if DEBUG:
            print()
            print()

        for elemento in elementos:                                                                                      # Recorriendo la lista elementos para buscar las posiciones que ocupan en la lista
            padres = elemento.padres()                                                                                  # Obteniendo padres

            conexiones = elemento.conexiones()                                                                          # Obteniendo conexiones

            if padres != []:
                elemento.padres(ventana_modelo.convertir_padres_a_elementos(elementos, padres), True)

            if conexiones != []:
                elemento.conexiones(ventana_modelo.convertir_conexiones_a_elementos(elementos, conexiones), True)

        if DEBUG:
            print('Listando datos después de ser almacenados en memoria...')

            for elemento in elementos:
                print(elemento.nombre(), 'es una máquina con duración', elemento.duracion())

                for padre in elemento.padres():
                    print("\tPadre:", padre.nombre())

                for conexion in elemento.conexiones():
                    print("\tConexión: ", conexion['objeto'].nombre(), ', ', conexion['duracion'], sep = '')

            print()
            print()

        return elementos


    @staticmethod                                                                                                       # Método estático
    def procesar(texto):                                                                                                # Procesa un texto: convierte un texto en formato NTriples a grafo
        grafo = Graph()

        try:
            grafo.parse(data = texto, format = 'n3')

        except:
            res = None

        else:
            res = grafo

        finally:
            return res


    @staticmethod                                                                                                       # Método estático
    def podar(soluciones):                                                                                              # "Poda" (elimina elementos no válidos de) la lista de soluciones
        for solucion in soluciones:                                                                                     # Recorriendo la lista de soluciones
            if len(solucion.camino()) == 0:                                                                             # Criterio de eliminación: el camino tiene una longitud de cero nodos
                soluciones.remove(solucion)

        return soluciones
