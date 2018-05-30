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


class ventana_modelo():
    @staticmethod
    def interpretar(grafo):
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
                print(fila.name, 'es una máquina', 'con duración', fila.duracion)

        if DEBUG:
            print()


    @staticmethod
    def procesar(texto):
        grafo = Graph()

        try:
            grafo.parse(data = texto, format = 'n3')

        except:
            res = None

        else:
            res = grafo

        finally:
            return res
