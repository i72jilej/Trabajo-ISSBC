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


import sys                                                  # Funcionalidades varias del sistema

import vista

if sys.version_info[0] < 3:
    from io import open

# from PyQt4 import QtGui


class ventana_principal(vista.ventana_vista):
    _modificado = False                                     # Inicialización de variables de clase


    def __init__(self):                                     # Constructor de la clase
        if sys.version_info[0] >= 3:                        # Llamada al método equivalente de la clase padre
            super().__init__()
        else:
            super(ventana_principal, self).__init__()


    def abrir(self):                                        # Acción de abrir 
        respuesta = self.confirmar_modificado()

        if respuesta == vista.respuestas.diccionario[vista.respuestas.DESCARTAR]:
            self.apertura()

        elif respuesta == vista.respuestas.diccionario[vista.respuestas.GUARDAR]:
            if self.guardar():
                self.apertura()

            else:
                pass

        else:
            pass


    def apertura(self):                                     # Procedimiento de apertura
        if sys.version_info[0] >= 3:                        # Llamada al método equivalente de la clase padre
            nombre_archivo = super().apertura()
        else:
            nombre_archivo = super(ventana_principal, self).apertura()

        if nombre_archivo != '':                                        # Comprobando si se ha elegido algún archivo
            try:                                                        #Si se ha elegido un archivo
                archivo = open(file = nombre_archivo, mode = 'r', encoding = 'utf-8')

            except IOError:
                res = False

            else:
                texto = archivo.read()

                self.modificado(False)

                # TODO: Interpretar archivo (rdflib) y controlar si es correcto

                # FIXME: Borrar
                self._text_desarrollo.setText(texto)
                self._grafo = texto

                if sys.version_info[0] >= 3: 
                    self.setWindowTitle(self._TITULO_APP + ' ➡ ' + nombre_archivo) 
                else: 
                    self.setWindowTitle(self._TITULO_APP + u' ➡ ' + nombre_archivo) 

                res = True

            finally:
                try:
                    archivo.close()

                except UnboundLocalError:
                    pass

                return res


    def calcular(self):                                     # Realiza los cálculos necesarios
        try:
            self._grafo

        except AttributeError:
            if sys.version_info[0] >= 3:                    # Llamada al método equivalente de la clase padre
                super().calcular()
            else:
                super(ventana_principal, self).calcular()

        else:
            #TODO: Por hacer

            self._modificado = True

        finally:
            pass


    def closeEvent(self, event):                            # Se pregunta al usuario si quiere salir
        respuesta = self.confirmar_modificado()

        if respuesta == vista.respuestas.diccionario[vista.respuestas.DESCARTAR]:
            event.accept()

        elif respuesta == vista.respuestas.diccionario[vista.respuestas.GUARDAR]:
            if self.guardar():
                event.accept()

            else:
                event.ignore()

        else:
            event.ignore()


    def guardado(self):                                     # Procedimiento de guardado
        try:
            archivo = open(file = self._nombre_archivo, mode = 'w', encoding = 'utf-8')

        except IOError:
            if sys.version_info[0] >= 3:                    # Llamada al método equivalente de la clase padre
                super().guardado()
            else:
                super(ventana_principal, self).guardado()

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


    def guardar_como(self):                                 # Acción de guardar cómo
        if sys.version_info[0] >= 3:                        # Llamada al método equivalente de la clase padre
            self._nombre_archivo = super().guardar_como()
        else:
            self._nombre_archivo = super(ventana_principal, self).guardar_como()

        if self._nombre_archivo != '':
            return self.guardado()
        else:
            return False


    def limpiar(self):                                      # Acción de limpiar
        self._text_ruta.clear()
        self._text_solucion.clear()
        self._text_desarrollo.clear()
        self._text_dominio.clear()

        self.modificado(False)

        self.setWindowTitle(self._TITULO_APP)

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

        if respuesta == vista.respuestas.diccionario[vista.respuestas.DESCARTAR]:
            self.limpiar()

        elif respuesta == vista.respuestas.diccionario[vista.respuestas.GUARDAR]:
            if self.guardar():
                self.limpiar()

            else:
                pass

        else:
            pass


