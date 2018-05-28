#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Title         : controlador.py
# Description   : Controlador del programa
# Author        : Julio Domingo Jiménez Ledesma
# Author        : Rafael Carlos Méndez Rodríguez
# Date          : 29-05-2018
# Version       : 1.0.0
# Usage         : import controlador o from controlador import ...
# Notes         : 


TITULO_APP = 'Planificador de cadena de montaje'


import sys

from PyQt4 import QtGui


class ventana_controlador():
    _modificado = False                                     # Inicialización de variables de clase


    def __init__(self):                                     # Constructor de la clase
        pass


    def abrir(self):                                        # Acción de abrir
        respuesta = self.confirmar_modificado()

        if respuesta == QtGui.QMessageBox.Discard:
            self.apertura()
        elif respuesta == QtGui.QMessageBox.Save:
            if self.guardar():
                self.apertura()
            else:
                pass
        else:
            pass


    def apertura(self):
        nombre_archivo = QtGui.QFileDialog.getOpenFileName(self, 'Abrir archivo', filter = 'Archivo N-Triples (*.nt);;Todos los archivos (*.*)')

        # try:
        if nombre_archivo != '':
            try:
                archivo = open(file = nombre_archivo, mode = 'r', encoding = 'utf-8')

            except IOError:
                QtGui.QMessageBox.warning(self, 'Error de apertura', 'Error: Archivo <' + nombre_archivo + '> inaccesible')

            else:
                self._texto = archivo.read()

                # FIXME: Así no
                self._text_desarrollo.setText(self._texto)
                
                self._text_ruta.setText(nombre_archivo)

                self.modificado(False)

                if sys.version_info[0] >= 3:
                    self.setWindowTitle(TITULO_APP + ' ➡ ' + nombre_archivo)
                else:
                    self.setWindowTitle(TITULO_APP + u' ➡ ' + nombre_archivo)

            finally:
                try:
                    archivo.close()

                except UnboundLocalError:
                    pass

                return True

        # except AttributeError:
            # return False

        pass


    def calcular(self):                                     # Realiza los cálculos necesarios
        try:
            self._texto

        except AttributeError:
            QtGui.QMessageBox.information(self, 'Error de cálculo', 'Error: No se ha cargado ningún archivo')

        else:
            #TODO: Por hacer

            self._modificado = True

        finally:
            pass


    def closeEvent(self, event):                            # Se pregunta al usuario si quiere salir
        respuesta = self.confirmar_modificado()

        if respuesta == QtGui.QMessageBox.Discard:
            event.accept()

        elif respuesta == QtGui.QMessageBox.Save:
            if self.guardar():
                event.accept()

            else:
                event.ignore()

        else:
            event.ignore()


    def confirmar_modificado(self):
        # TODO: Ponerle nombre a los botones

        if self.modificado():
            if sys.version_info[0] >= 3:
                return QtGui.QMessageBox.question(self, 'Aviso', 'Hay cálculos no guardados. ¿Desea guardarlos antes de salir?', QtGui.QMessageBox.Discard | QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)
            else:
                return QtGui.QMessageBox.question(self, 'Aviso', u'Hay cálculos no guardados. ¿Desea guardarlos antes de salir?', QtGui.QMessageBox.Discard | QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

        else:
            return QtGui.QMessageBox.Discard


    def guardado(self):
        try:
            archivo = open(file = self._nombre_archivo, mode = 'w', encoding = 'utf-8')

        except IOError:
            QtGui.QMessageBox.warning(self, 'Error de apertura', 'Error: Archivo <' + self._nombre_archivo + '> inaccesible')

            return False


        else:
            # FIXME: Así tampoco archivo.write(self.textEdit.toPlainText())

            self.modificado(False)

            return True

        finally:
            # TODO: Comprobar si se llega aquí

            archivo.close()


    def guardar(self):                                      # Acción de guardar
        try:
            self._nombre_archivo

        except AttributeError:
            return self.guardarComo()

        else:
            if self._nombre_archivo == '':
                del self._nombre_archivo

                return self.guardarComo()

            else:
                return self.guardado()

        finally:
            pass

        return True


    def guardarComo(self):
        self._nombre_archivo = QtGui.QFileDialog.getSaveFileName(self, 'Guardar archivo')

        if self._nombre_archivo != '':
            return self.guardado()
        else:
            return False


    def imprimir(self):                                     # Acción de imprimir
        impresion = QtGui.QPrintDialog()

        if impresion.exec_() == QtGui.QDialog.Accepted:
            # TODO: Establecer widget a imprimir self.textEdit.document().print_(impresion.printer())
            pass

        else:
            pass


    def limpiar(self):                                      # Acción de limpiar
        self._text_ruta.clear()
        self._text_solucion.clear()
        self._text_desarrollo.clear()
        self._text_dominio.clear()

        self.modificado(False)

        self.setWindowTitle(TITULO_APP)

        try:
            del self._nombre_archivo

        except AttributeError:
            pass



    def modificado(self, *args):                            # Función "sobrecargada": modificador / observador de la variable self._modificado
        if args != ():
            self._modificado = args[0]

        else:
            pass

        return self._modificado


    def nuevo(self):                                        # Acción de nuevo
        respuesta = self.confirmar_modificado()

        if respuesta == QtGui.QMessageBox.Discard:
            self.limpiar()

        elif respuesta == QtGui.QMessageBox.Save:
            if self.guardar():
                self.limpiar()

            else:
                pass

        else:
            pass


