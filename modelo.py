#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Title         : modelo.py
# Description   : Modelo del programa
# Author        : Julio Domingo Jiménez Ledesma
# Author        : Rafael Carlos Méndez Rodríguez
# Date          : 15-06-2018
# Version       : 1.0.1
# Usage         : import modelo o from modelo import ...
# Notes         : 


from __future__ import print_function


DEBUG       = True
DEBUG_HIJOS = False

ESPERA = 1                                                                                                                              # Tiempo de espera para que el padre compruebe la finalización de sus hijos


import os                                                                                                                               # Funcionalidades varias del sistema operativo
import random                                                                                                                           # Generación de números aleatorios

if DEBUG:
    import sys                                                                                                                          # Funcionalidades varias del sistema

from threading import Thread                                                                                                            # Capacidades multihilo
from time import sleep                                                                                                                  # Pausas

from rdflib import Graph                                                                                                                # Grafos


class Element():                                                                                                                        # Representacion de un nodo en el grafo
    def __init__(self, id_elemento, nombre, duracion):                                                                                  # Constructor de la clase
        self._id_elemento = id_elemento                                                                                                 # Inicialización de variables

        self._nombre = nombre

        self._duracion = duracion

        self._padres = []

        self._conexiones = []


    def conexion(self, elemento):
        res = None

        for conexion in self._conexiones:
            if conexion['objeto'] == elemento:
                res = conexion

                break

        return res


    def conexiones(self, conexion = None, multiples = False):                                                                           # Método "sobrecargado":
        if conexion != None:                                                                                                            #     Modificador de la variable
            if multiples == True:                                                                                                       #     Modificador múltiple
                self._conexiones = conexion

            else:                                                                                                                       #     Modificador simple
                self._conexiones.append(conexion)

        return self._conexiones                                                                                                         #     Observador de la variable


    def duracion(self, duracion = None):                                                                                                # Método "sobrecargado":
        if duracion != None:                                                                                                            #     Modificador de la variable
            self._duracion = duracion

        return self._duracion                                                                                                           #     Observador de la variable


    def id_elemento(self, id_elemento = None):                                                                                          # Método "sobrecargado":
        if id_elemento != None:                                                                                                         #     Modificador de la variable
            self._id_elemento = id_elemento

        return self._id_elemento                                                                                                        #     Observador de la variable


    def nombre(self, nombre = None):                                                                                                    # Método "sobrecargado":
        if nombre != None:                                                                                                              #     Modificador de la variable
            self._nombre = nombre

        return self._nombre                                                                                                             #     Observador de la variable


    def padres(self, padre = None, multiples = False):                                                                                  # Método "sobrecargado":
        if padre != None:                                                                                                               #     Modificador de la variable
            if multiples == True:                                                                                                       #     Modificador múltiple
                self._padres = padre

            else:                                                                                                                       #     Modificador simple
                self._padres.append(padre)

        return self._padres                                                                                                             #     Observador de la variable


class solucion():                                                                                                                       # Representación de una solución
    def __init__(self):                                                                                                                 # Constructor de la clase
        self._camino = []                                                                                                               # Inicialización de variables

        self._duracion = 0


    def anyadir(self, nodo):                                                                                                            # Añade un nodo a la solución, siempre que éste no esté ya en ella
        try:
            self._camino.index(nodo)                                                                                                    # Comprobación de que no esté ya añadido

        except ValueError:                                                                                                              # En caso de no estarlo:
            self.__duracion(nodo)                                                                                                       #     Se recalcula la duración de la solución

            self._camino.append(nodo)                                                                                                   #     Y se añade el nodo

            res = True                                                                                                                  #     Se prepara el "informe"

        else:                                                                                                                           # En caso de estar repetido:
            res = False                                                                                                                 #     Se prepara el "informe"

        finally:
            return res                                                                                                                  # Se devuelve el informe del éxito (o no) del añadido


    def camino(self):                                                                                                                   # Observador de la variable
        return self._camino                                                                                                             # Se entiende que un camino no se modificará (a excepción de añadir nuevos nodos al mismo)


    def duracion(self):                                                                                                                 # Observador de la variable
        return self._duracion


    def invalidar(self):                                                                                                                # Marca la solución como no válida
        self._camino = []


    def validar(self):                                                                                                                  # Autovalidador de la solución (atendiendo a los requisitos de otras máquinas)
        nodos_visitados = []

        res = True

        for nodo in self._camino:
            padres = nodo.padres()

            if padres != []:
                for padre in padres:
                    try:
                        nodos_visitados.index(padre)                                                                                    # Buscando al padre en los nodos ya visitados

                    except ValueError:                                                                                                  # Si el padre no se encuentra
                        res = False

                    else:
                        # res = True
                        res = res and True

                    finally:
                        if res == False:
                            break

            else:
                pass

            if res == False:
                break

            nodos_visitados.append(nodo)

        if res == False:
            self.invalidar()                                                                                                            # Camino vacío significa camino no válido (se podará más adelante)

        return res


    def __duracion(self, nodo):                                                                                                         # Método interno para el recálculo de la duración de la solución
        if self._camino != []:                                                                                                          # Si existe un camino
            for conexion in self._camino[len(self._camino) - 1].conexiones():                                                           #     Se calcula la duración de la conexión entre el útimo nodo del mismo y el que se añadirá
                if conexion['objeto'] == nodo:
                    duracion_conexion = conexion['duracion']

                    break

        else:                                                                                                                           # Si no:
            duracion_conexion = 0                                                                                                       #     La duración es cero


        self._duracion += duracion_conexion + nodo.duracion()                                                                           # La duración será la que actualmente haya más la duración de la conexión más la duración del nodo que se añadirá


    def __repr__(self):
        return str([nodo.nombre() for nodo in self._camino])


class ventana_modelo():                                                                                                                 # Parte del modelo de la ventana
    def anyadir_solucion(self):                                                                                                         # Añade una solución a la lista de soluciones
        tiempo = 0

        nodos = self._solucion_elegida.camino()

        num_nodos = len(nodos)

        for i in range(num_nodos):
            conexiones = nodos[i].conexiones()                                                                                          # Obteniendo las conexiones de la máquina

            if i < num_nodos - 1:
                tiempo += nodos[i].duracion() + conexiones[conexiones.index(nodos[i].conexion(nodos[i + 1]))]['duracion']               # Calculando el tiempo = tiempo de la máquina + tiempo de la conexión a la siguiente

        self._soluciones.append(self._solucion_elegida)


    def calcular(self):                                                                                                                 # Cálculo de soluciones
        hijos = list()

        self._soluciones_posibles = [solucion() for i in range(self._num_hijos)]                                                                  # Inicialización de la lista de soluciones

        nodos_iniciales = self.iniciales(self._datos)                                                                                   # Precáculo de los nodos iniciales

        for i in range(self._num_hijos):
            if DEBUG_HIJOS:
                print('Padre #', os.getpid(), "\tPreparando hijo ", i, sep = '')

            hijos.append(Thread(target = ventana_modelo.calcular_hijos, args = (self, i, nodos_iniciales,)))                            # Declarando los hijos; ejecutarán ventana_modelo.calcular_hijos

            if DEBUG_HIJOS:
                print('Padre #', os.getpid(), "\tArrancando hijo ", i, sep = '')

            hijos[i].start()

        while hijos:                                                                                                                    # Mientras la lista tenga hijos
            aux = []

            for hijo in hijos:                                                                                                          # Para cada hijo de la lista
                if not hijo.is_alive():                                                                                                 # Comprobación de si el hijo ha finalizado
                    hijo.join()                                                                                                         # Se recupera el proceso y se saca de la lista
                    aux.append(hijo)

            for hijo in aux:
                hijos.remove(hijo)

                del(hijo)

            if DEBUG == True:
                print('Padre #', os.getpid(), "\tEsperando a que los procesos hijos hagan su trabajo", sep = '')

            sleep(ESPERA)                                                                                                               # Para no saturar, el padre queda en espera durante "ESPERA" segundos

        if DEBUG == True:
            print()
            print()

        self._soluciones_posibles = self.podar(self._soluciones_posibles)                                                               # Primera "poda"

        if DEBUG == True:
            for una_solucion in self._soluciones_posibles:                                                                              # Recorriendo la lista con las soluciones dadas por los hijos
                print('Padre #', os.getpid(), "\tSolución posible: ", [nodo.nombre() for nodo in una_solucion.camino()], sep = '')

            print()
            print()

        self._soluciones_candidatas = self.validar(self._soluciones_posibles)

        del self._soluciones_posibles

        if self._soluciones_candidatas != []:
            if DEBUG == True:
                for una_solucion in self._soluciones_candidatas:                                                                            # Recorriendo la lista con las soluciones dadas por los hijos
                    if sys.version_info[0] >= 3:
                        print('Padre #', os.getpid(), "\tSolución candidata: ", [str(nodo.nombre()) for nodo in una_solucion.camino()], sep = '')

                    else:
                        print('Padre #', os.getpid(), "\tSolución candidata: ", [nodo.nombre().toPython() for nodo in una_solucion.camino()], sep = '')

                print()
                print()


            self._solucion_elegida = self.elegir(self._soluciones_candidatas, self._prob_heuristica)

            self.anyadir_solucion()

            if DEBUG:
                for una_solucion in self._soluciones:
                    if sys.version_info[0] >= 3:
                        print('Padre #', os.getpid(), "\tSolución definitiva: ", [str(nodo.nombre()) for nodo in una_solucion.camino()], sep = '')

                    else:
                        print('Padre #', os.getpid(), "\tSolución definitiva: ", [nodo.nombre().toPython() for nodo in una_solucion.camino()], sep = '')

            print()
            print()


    def calcular_hijos(self, id_hijo, nodos_iniciales):                                                                                 # Cálculo de cada solución (ejecutada por cada hijo)
        if DEBUG_HIJOS:
            print('Hijo  #', id_hijo, "\tHe sido llamado", sep = '')

        longitud_datos = len(self._datos)                                                                                               # Precarga de la longitud del camino

        nodo_elegido = self.elegir(nodos_iniciales, self._prob_heuristica)

        self._soluciones_posibles[id_hijo].anyadir(nodo_elegido)                                                                        # Se añade un nodo inicial en función del la probabilidad de emplear la heurística

        if DEBUG_HIJOS:
            print('Hijo  #', id_hijo, "\tAñadido al camino el nodo ", nodo_elegido.nombre(), sep = '')

        while len(self._soluciones_posibles[id_hijo].camino()) < longitud_datos:                                                        # Mientras queden máquinas por las que pasar
            if DEBUG_HIJOS:
                print('Hijo  #', id_hijo, "\tEl tamaño del árbol es de ", longitud_datos, ' nodos', sep = '')
                print('Hijo  #', id_hijo, "\tEl tamaño del camino es de ", len(self._soluciones_posibles[id_hijo].camino()), ' nodos', sep = '')


            conexiones = self._soluciones_posibles[id_hijo].camino()[len(self._soluciones_posibles[id_hijo].camino()) - 1].conexiones() # Lista de tuplas: (hijo, duracion)

            nodos_conexiones = [conexion['objeto'] for conexion in conexiones]                                                          # "Desempaquetado" en dos listas

            nodo_elegido = self.elegir(nodos_conexiones, self._prob_heuristica)

            if DEBUG_HIJOS:
                print('Hijo  #', id_hijo, "\tIntentando añadir al camino el nodo ", nodo_elegido.nombre(), sep = '')

            valido = self._soluciones_posibles[id_hijo].anyadir(nodo_elegido)

            while not valido:
                if DEBUG_HIJOS:
                    print('Hijo  #', id_hijo, "\tNo es posible", sep = '')

                nodos_conexiones.remove(nodo_elegido)

                if nodos_conexiones != []:
                    nodo_elegido = self.elegir(nodos_conexiones, self._prob_heuristica)

                    if DEBUG_HIJOS:
                        print('Hijo  #', id_hijo, "\tIntentando añadir al camino el nodo ", nodo_elegido.nombre(), sep = '')

                    valido = self._soluciones_posibles[id_hijo].anyadir(nodo_elegido)                                                   # Se añade un nodo siguiente en función del la probabilidad de emplear la heurística

                else:
                    self._soluciones_posibles[id_hijo] = solucion()

                    return


    @staticmethod                                                                                                                       # Método estático
    def convertir_conexiones_a_elementos(elementos, conexiones):                                                                        # Conversor de nombres a ids aplicado a conexiones
        res = []

        for conexion in conexiones:
            for id_elemento in range(len(elementos)):
                if elementos[id_elemento].nombre() == conexion[0]:
                    objeto_conexion = {'objeto': elementos[id_elemento], 'duracion': conexion[1]}

                    break

            res.append(objeto_conexion)

        return res


    @staticmethod                                                                                                                       # Método estático
    def convertir_padres_a_elementos(elementos, padres):                                                                                # Conversor de nombres a ids aplicado a padres
        res = []

        for padre in padres:
            for id_elemento in range(len(elementos)):
                if elementos[id_elemento].nombre() == padre:
                    objeto_padre = elementos[id_elemento]

                    break

            res.append(objeto_padre)

        return res


    @staticmethod
    def elegir(nodos, prob_heuristica):                                                                                                 # Se elige un nodo en función del la probabilidad de emplear la heurística
        ''' Se elige un nodo en función del la probabilidad de emplear la heurística:
                Si no se emplea, se elige un hijo aleatoriamente
                Si sí, se elige al mejor en función de la duración de los mismos
        '''
        duraciones = [nodo.duracion() for nodo in nodos]                                                                                # "Desempaquetado" en dos listas

        return \
            random.choice(nodos) \
            if random.randint(0, 100) > prob_heuristica \
            else nodos[duraciones.index(min(duraciones))]


    @staticmethod                                                                                                                       # Método estático
    def iniciales(datos):                                                                                                               # Devuelve una lista con las ids de los nodos padres y sus respectivas duraciones
        res = []

        for nodo in datos:
            if nodo.padres() == []:
                res.append(nodo)

        return res


    @staticmethod                                                                                                                       # Método estático
    def interpretar(grafo):                                                                                                             # Interpreta un grafo dado: extrae la información necesaria para su posterior uso
        if DEBUG:
            print('Listando datos antes de ser almacenados en memoria...')

        elementos = []
        #                                                                                                                               # Extrayendo máquinas del grafo
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

        for fila in resultado:                                                                                                          # Para cada máquina...
            if DEBUG:
                print(fila.nombre, 'es una máquina con duración', fila.duracion)

            if sys.version_info[0] >= 3:
                texto = str(fila.nombre)

            else:
                texto = fila.nombre.toPython().encode('utf-8')

            elemento = Element(len(elementos), texto, int(fila.duracion))                                                               # Almacenando la máquina como un Element

            #                                                                                                                           # Buscando padres de la máquina...
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

            for subfila in subresultado:                                                                                                # Recorriendo la lista de padres
                if DEBUG:
                    print("\tPadre:", subfila.nombre_padre)

                if sys.version_info[0] >= 3:
                    texto = str(subfila.nombre_padre)

                else:
                    texto = subfila.nombre_padre.toPython().encode('utf-8')

                elemento.padres(texto)                                                                                                  # Almancenando el nombre del padre de la máquina en el Element
            #                                                                                                                           # Buscando las conexiones de la máquina
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

            for subfila in subresultado:                                                                                                # Recorriendo la lista de conexiones
                if DEBUG:
                    print("\tConexión: ", subfila.nombre_siguiente, ', ', subfila.duracion, sep = '')

                if sys.version_info[0] >= 3:
                    texto = str(subfila.nombre_siguiente)

                else:
                    texto = subfila.nombre_siguiente.toPython().encode('utf-8')

                elemento.conexiones((texto, int(subfila.duracion)))                                                                     # Almacenando las conexiones en el Element

            elementos.append(elemento)                                                                                                  # Almacenando el Element elemento en la lista elementos -> Lista manejada

        if DEBUG:
            print()
            print()

        for elemento in elementos:                                                                                                      # Recorriendo la lista elementos para buscar las posiciones que ocupan en la lista
            padres = elemento.padres()                                                                                                  # Obteniendo padres

            conexiones = elemento.conexiones()                                                                                          # Obteniendo conexiones

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


    @staticmethod                                                                                                                       # Método estático
    def procesar(texto):                                                                                                                # Procesa un texto: convierte un texto en formato NTriples a grafo
        grafo = Graph()

        try:
            grafo.parse(data = texto, format = 'n3')

        except:
            res = None

        else:
            res = grafo

        finally:
            return res


    @staticmethod                                                                                                                       # Método estático
    def podar(soluciones):                                                                                                              # "Poda" (elimina elementos no válidos de) la lista de soluciones
        aux = []

        for solucion in soluciones:                                                                                                     # Recorriendo la lista de soluciones
            if len(solucion.camino()) == 0:                                                                                             # Criterio de eliminación: el camino tiene una longitud de cero nodos
                aux.append(solucion)

        for solucion in aux:
            soluciones.remove(solucion)

        return soluciones


    @staticmethod                                                                                                                       # Método estático
    def validar(soluciones):                                                                                                            # Valida las soluciones
        for solucion in soluciones:                                                                                                     # Recorre la lista de soluciones
            solucion.validar()                                                                                                          # Valida cada solución
            #                                                                                                                           # Validación de tipo "prerrequisitos"
        soluciones = ventana_modelo.podar(soluciones)                                                                                   # "Poda" las que no son válidas

        return soluciones


