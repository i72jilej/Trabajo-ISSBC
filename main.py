#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Title         : main.py
# Description   : Lanzador del programa
# Author        : Julio Domingo Jiménez Ledesma
# Author        : Rafael Carlos Méndez Rodríguez
# Date          : 23-05-2018
# Version       : 1.0.0
# Usage         : python main.py
# Notes         : 


import sys                                                  # Funcionalidades varias del sistema

import vista                                                # Módulo vista

from PyQt4 import QtGui


def main(argv):
    aplicacion = QtGui.QApplication(argv)

    ventana = vista.ventana_principal()
    # ventana.show()
    ventana.showMaximized()                                 # Mejor maximizada

    sys.exit(aplicacion.exec_())


if __name__ == '__main__':
    main(sys.argv)
