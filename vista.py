#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Title         : vista.py
# Description   : Vista del programa
# Author        : Julio Domingo Jiménez Ledesma
# Author        : Rafael Carlos Méndez Rodríguez
# Date          : 23-05-2018
# Version       : 0.0.1
# Usage         : import vista o from vista import ...
# Notes         : 


TITULO_APP = 'Planificador de cadena de montaje'


from PyQt4 import QtGui


class ventana_compositor():
    def dibujar_iu(self):
        # TODO: Widgets self.textEdit = editor()

        # TODO: ¿Eventos? self.textEdit.textChanged.connect(self.textoModificado)

        # Etiquetas
        carpeta = QtGui.QLabel('Carpeta')
        espacio = QtGui.QLabel('                   ')

        # Controles de edición
        self._carpetaEdit = QtGui.QLineEdit()
        self._carpetaEdit.setReadOnly(True)

        # Controles listWidget
        self._listaArchivos = QtGui.QListWidget()           # Crea un listwidget
        # self._listaArchivos.clicked.connect(self.cargado)

        # Botones
        self.folder = QtGui.QPushButton('Seleccionar')      # Crea el botón de seleccionar carpeta
        self.folder.clicked.connect(self.abrir)             # Conecta el botón con su función

        buttonLayout = QtGui.QHBoxLayout()                  # Crea un contenedor de botones vertical

        self.buttons = []                                   # Crea una lista para almacenar los botones

        for text, slot in (('Guardar', self.guardar),
                           ('Guardar como', self.guardarComo)):
            self.buttons.append(QtGui.QPushButton(text))    # Añade a la lista el botón

            buttonLayout.addStretch()
            buttonLayout.addWidget(self.buttons[-1])        # Añade el botón a la rejilla
            self.buttons[-1].clicked.connect(slot)          # Conecta el botón con el slot

        # Rejillas de distribución
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(espacio, 0, 0)
        grid.addWidget(espacio, 0, 1)
        grid.addWidget(espacio, 0, 2)
        grid.addWidget(espacio, 0, 3)
        grid.addWidget(espacio, 0, 4)

        grid.addWidget(carpeta, 1, 0)
        grid.addWidget(self._carpetaEdit, 1, 1, 1, 3)
        grid.addWidget(self.folder, 1, 4)

        grid.addWidget(self._listaArchivos, 3, 0)
        # grid.addWidget(self.textEdit, 3, 1, 1, 4)

        editionLayout = QtGui.QVBoxLayout()                 # Crea una rejilla de botones vertical
        editionLayout.addItem(grid)

        self.principalLayout = QtGui.QVBoxLayout()          # Crea una rejilla de botones Horizoontal
        self.principalLayout.addStretch()
        self.principalLayout.addLayout(editionLayout)
        self.principalLayout.addLayout(buttonLayout)

        # self.setGeometry(300, 300, 350, 300)                # Los parámetros de tamaño vistos son suficientes
