#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Title         : controlador.py
# Description   : Controlador del programa
# Author        : Julio Domingo Jiménez Ledesma
# Author        : Rafael Carlos Méndez Rodríguez
# Date          : 23-05-2018
# Version       : 0.0.1
# Usage         : import controlador o from controlador import ...
# Notes         : 


from PyQt4 import QtGui


class ventana_controlador():
    # Inicialización de variables de clase
    _modificado = False


    def abrir(self):
        respuesta = self.confirmarModificado()

        if respuesta == QtGui.QMessageBox.Discard or respuesta == True:
            self.apertura()
        elif respuesta == QtGui.QMessageBox.Save:
            if self.guardar():
                self.apertura()
            else:
                pass
        else:
            pass


    def closeEvent(self, event):                            # Se pregunta al usuario si quiere salir
        respuesta = self.confirmarModificado()

        if respuesta == QtGui.QMessageBox.Discard or respuesta == True:
            event.accept()
        elif respuesta == QtGui.QMessageBox.Save:
            if self.guardar():
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()


    def guardar(self):
        try:
            self._nombre_archivo

        except AttributeError:
            return self.guardarComo()

        else:
            return self.guardado()

        finally:
            pass

        return True


    def modificado(self, *args):
        if args != ():
            self._modificado = args[0]

            return True
        else:
            return self._modificado

