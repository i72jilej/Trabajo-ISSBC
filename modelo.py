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

import os                                                       # Funcionalidades varias del sistema operativo

from threading import Thread                                    # Capacidades multihilo

from rdflib import Graph


class Element():                                                # Representacion de un nodo en el grafo
    def __init__(self, nombre, duracion):                       # Constructor de la clase
        self._nombre = nombre                                   # Inicialización de variables

        self._duracion = duracion

        self._padres = []

        self._conexiones = []


    def conexiones(self, conexion = None, multiples = False):   # Método "sobrecargado":
        if conexion != None:                                    #     Modificador de la variable
            if multiples == True:                               #     Modificador múltiple
                self._conexiones = conexion

            else:                                               #     Modificador simple
                self._conexiones.append(conexion)

        return self._conexiones                                 #     Observador de la variable


    def duracion(self, duracion = None):                        # Método "sobrecargado":
        if duracion != None:                                    #     Modificador de la variable
            self._duracion = duracion

        return self._duracion                                   #     Observador de la variable


    def nombre(self, nombre = None):                            # Método "sobrecargado":
        if nombre != None:                                      #     Modificador de la variable
            self._nombre = nombre

        return self._nombre                                     #     Observador de la variable


    def padres(self, padre = None, multiples = False):          # Método "sobrecargado":
        if padre != None:                                       #     Modificador de la variable
            if multiples == True:                               #     Modificador múltiple
                self._padres = padre

            else:                                               #     Modificador simple
                self._padres.append(padre)

        return self._padres                                     #     Observador de la variable


class ventana_modelo():                                         # Parte del modelo de la ventana
    def calcular(self, hilos):
        hijos = list()

        for i in range(hilos):
            if DEBUG:
                print('Padre #', os.getpid(), "\tPreparando hijo ", i, sep = '')

            hijos.append(Thread(target = ventana_modelo.calcular_hijos, args = (i, datos,)))

            if DEBUG:
                print('Padre #', os.getpid(), "\tArrancando hijo ", i, sep = '')

            hijos[i].start()

        for hijo in hijos:
            hijo.join()


        if DEBUG:
            print('Hijo  #', id_hijo, "\tHe sido llamado", sep = '')


    @staticmethod                                               # Método estático
    def convertir_conexiones_a_ids(elementos, conexiones):      # Conversor de nombres a ids aplicado a conexiones
        res = []

        for conexion in conexiones:
            id_conexion = -1

            for id_elemento in range(len(elementos)):
                if elementos[id_elemento].nombre() == conexion[0]:
                    id_conexion = id_elemento

                    break

            res.append((id_conexion, conexion[1]))

        return res


    @staticmethod                                               # Método estático
    def convertir_padres_a_ids(elementos, padres):              # Conversor de nombres a ids aplicado a padres
        res = []

        for padre in padres:
            id_padre = -1

            for id_elemento in range(len(elementos)):
                if elementos[id_elemento].nombre() == padre:
                    id_padre = id_elemento

                    break

            res.append(id_padre)

        return res


    @staticmethod                                               # Método estático
    def interpretar(grafo):                                     # Interpreta un grafo dado: extrae la información necesaria para su posterior uso
        if DEBUG:
            print('Listando datos antes de ser almacenados en memoria...')

        elementos = []

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

        for fila in resultado:
            if DEBUG:
                print(fila.nombre, 'es una máquina con duración', fila.duracion)

            elemento = Element(fila.nombre, fila.duracion)

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

            for subfila in subresultado:
                if DEBUG:
                    print("\tPadre de ", elemento.nombre(), ': ', subfila.nombre_padre, sep = '')

                elemento.padres(subfila.nombre_padre)

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

            for subfila in subresultado:
                if DEBUG:
                    print("\tConexión de ", elemento.nombre(), ': ', subfila.nombre_siguiente, ', ', subfila.duracion, sep = '')

                elemento.conexiones((subfila.nombre_siguiente, int(subfila.duracion)))

            elementos.append(elemento)

        if DEBUG:
            print()
            print()

        for elemento in elementos:
            padres = elemento.padres()

            conexiones = elemento.conexiones()

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


    @staticmethod                                               # Método estático
    def procesar(texto):                                        # Procesa un texto: convierte un texto en formato NTriples a grafo
        grafo = Graph()

        try:
            grafo.parse(data = texto, format = 'n3')

        except:
            res = None

        else:
            res = grafo

        finally:
            return res


