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


from rdflib import Graph


class Element():                                        # Representacion de un nodo en el grafo
    def __init__(self, nombre, duracion):               # Constructor de la clase
        self._nombre = nombre

        self._duracion = duracion

        self._conexiones = []

        self._padres = []

    
    def conexiones(self, conexion = None):              # Método "sobrecargado":
        if conexion != None:                            #     Modificador de la variable
            self._conexiones.append(conexion)

        return self._conexiones                         #     Observador de la variable


    def duracion(self, duracion = None):                # Método "sobrecargado":
        if duracion != None:                            #     Modificador de la variable
            self._duracion = duracion

        return self._duracion                           #     Observador de la variable


    def nombre(self, nombre = None):                    # Método "sobrecargado":
        if nombre != None:                              #     Modificador de la variable
            self._nombre = nombre

        return self._nombre                             #     Observador de la variable


    def padres(self, padre = None):                     # Método "sobrecargado":
        if padre != None:                               #     Modificador de la variable
            self._padres.append(padre)

        return self._padres                             #     Observador de la variable


class ventana_modelo():
    @staticmethod                                       # Método estático
    def interpretar(grafo):                             # Interpreta un grafo dado: extrae la información necesaria para su posterior uso
        elementos = []

        query = '''
                    PREFIX    rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns>
                    PREFIX    maquina:  <http://www.factory.fake/maquina/>
                    SELECT    ?name ?duracion

                    WHERE {
                        ?x    rdf:type            maquina:maquina    .
                        ?x    maquina:name        ?name              .
                        ?x    maquina:duracion    ?duracion          .
                        }

                    # ORDER BY ?name
                '''

        resultado = grafo.query(query)

        for fila in resultado:
            if DEBUG:
                print(fila.name, 'es una máquina con duración', fila.duracion)

            elemento = Element(fila.name, fila.duracion)

            query = '''
                        PREFIX    rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns>
                        PREFIX    maquina:  <http://www.factory.fake/maquina/>
                        SELECT    ?padre ?padreName

                        WHERE {
                            ?x      maquina:name        "%s"          .
                            ?x      maquina:padre       ?padre        .
                            ?padre  maquina:name        ?padreName    .
                            }
                    '''
                    # FIXME: Ver si nos vale así (usar solo ?padre, que es la ID interna o ?padreName que es el nombre de la maquina)

            subresultado = grafo.query(query % fila.name)

            for fila in subresultado:
                if DEBUG:
                    print('Padre de ', elemento.nombre(), ': ', fila.padreName, sep = '') # FIXME: Usando ?padreName, ver si usar ?padre

                elemento.padres(fila.padre)

            elementos.append(elemento)

        if DEBUG:
            print()


    @staticmethod                                       # Método estático
    def procesar(texto):                                # Procesa un texto: convierte un texto en formato NTriples a grafo
        grafo = Graph()

        try:
            grafo.parse(data = texto, format = 'n3')

        except:
            res = None

        else:
            res = grafo

        finally:
            return res
