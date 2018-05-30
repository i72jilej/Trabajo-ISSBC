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


from rdflib import Graph


class ventana_modelo():
    def procesar(self, texto):
        grafo = Graph()

        grafo.parse(data = texto, format = 'n3')

        return grafo
