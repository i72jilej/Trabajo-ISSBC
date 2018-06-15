#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Title         : controlador.py
# Description   : Controlador del programa
# Author        : Julio Domingo Jiménez Ledesma
# Author        : Rafael Carlos Méndez Rodríguez
# Date          : 15-06-2018
# Version       : 1.1.0
# Usage         : import controlador o from controlador import ...
# Notes         : ...


from __future__ import unicode_literals


DEBUG   = False
SANGRIA = '        '


import sys                                                                          # Funcionalidades varias del sistema

import modelo                                                                       # Modelo del programa
import vista                                                                        # Vista del programa

if sys.version_info[0] < 3:
    from io import open


class ventana_principal(modelo.ventana_modelo, vista.ventana_vista):
    def __init__(self):                                                             # Constructor de la clase
        if sys.version_info[0] >= 3:                                                # Llamada al método equivalente de la clase padre
            super().__init__()

        else:
            super(ventana_principal, self).__init__()

        self._cronograma = None                                                     # Inicialización de variables de clase

        self._modificado = False

        self._soluciones = []

        self.__num_soluciones = 0                                                   # Usada para la condición de parada


    def abrir(self):                                                                # Acción de abrir
        respuesta = self.confirmar_modificado('cargar uno nuevo')

        if respuesta == vista.respuestas.diccionario[vista.respuestas.DESCARTAR]:
            self.apertura()

        elif respuesta == vista.respuestas.diccionario[vista.respuestas.GUARDAR]:
            if self.guardar():
                self.apertura()

            else:
                pass

        else:
            pass


    def apertura(self):                                                             # Procedimiento de apertura
        nombre_archivo = vista.ventana_vista.apertura(self, 'abrir')                # Llamada al método equivalente de la clase vista

        if nombre_archivo != '':                                                    # Comprobando si se ha elegido algún archivo
            try:                                                                    # Si se ha elegido un archivo
                archivo = open(file = nombre_archivo, mode = 'r', encoding = 'utf-8')

            except IOError:
                res = False

            else:
                texto_archivo = archivo.read()

                self.modificado(False)

                grafo = self.procesar(texto_archivo)

                if grafo != None:
                    self._datos = self.interpretar(grafo)                           # Extrayendo datos manejables del grafo

                    texto_archivo = ''                                              # Necesario para reutilizar la dichosa variable

                    for i in range(len(self._datos)):                               # Construyendo la descripción del dominio
                        texto_archivo += self._datos[i].nombre() + ' es una máquina con duración ' + str(self._datos[i].duracion()) + "\n"

                        for padre in self._datos[i].padres():
                            texto_archivo += SANGRIA + 'Requiere haber pasado por ' + padre.nombre() + '\n'

                        for conexion in self._datos[i].conexiones():
                            texto_archivo += SANGRIA + 'Puede enviar a ' + conexion['objeto'].nombre() + ' con una duración de ' + str(conexion['duracion']) + "\n"

                        texto_archivo += "\n"

                    if sys.version_info[0] >= 3:                                    # Llamada al método equivalente de la clase padre
                        super().apertura('dominio', texto_archivo, nombre_archivo)

                    else:
                        super(ventana_principal, self).apertura('dominio', texto_archivo, nombre_archivo)

                    res = True

                else:
                    if sys.version_info[0] >= 3:                                    # Llamada al método equivalente de la clase padre
                        nombre_archivo = super().apertura('error')

                    self.limpiar('total')

                    res = False

            finally:
                try:
                    archivo.close()

                except UnboundLocalError:
                    pass

                else:
                    pass

                finally:
                    pass

        return res


    def calcular(self):                                                             # Realiza los cálculos necesarios
        try:
            self._datos

        except AttributeError:
            vista.ventana_vista.calcular(self, 'error')                             # Llamada al método equivalente de la clase vista

        else:
            if self._modificado == True:
                respuesta = self.confirmar_modificado('realizar nuevos cálculos')

                if respuesta == vista.respuestas.diccionario[vista.respuestas.DESCARTAR]:
                    self.limpiar('parcial')

                    self.calcular_bucle()

                elif respuesta == vista.respuestas.diccionario[vista.respuestas.GUARDAR]:
                    if self.guardar():
                        self.limpiar('parcial')

                        self.calcular_bucle()

                    else:
                        pass

                else:
                    pass

            else:
                self.limpiar('parcial')

                self.calcular_bucle()

        finally:
            pass


    def calcular_bucle(self):
        self.calculo()

        while len(self._soluciones) > self.__num_soluciones and len(self._soluciones) <= 10:
            self.__num_soluciones += 1

            self.calculo()

        tam_soluciones = len(self._soluciones)

        texto = 'Se han podido generar ' + str(tam_soluciones) + " soluciones válidas simultáneas:\n"

        for i in range(tam_soluciones):
            str_camino = ''
            tiempo = self._soluciones[i].duracion()

            for nodo in self._soluciones[i].camino():
                if sys.version_info[0] >= 3:
                    str_camino += str(nodo.nombre()) + ' - '

                else:
                    str_camino += nodo.nombre().toPython().encode('utf-8') + ' - '

            texto += SANGRIA + str(i) + ': ' + str_camino[0:-3] + ', con una duración de ' + str(tiempo) + " seg.\n"

        vista.ventana_vista.calcular(self, 'solucion', texto)


    def calculo(self):                                                              # Acción de realizar los cálculos
        modelo.ventana_modelo.calcular(self)                                        # Llamada al método equivalente de la clase vista

        texto = 'Se han generado ' + str(self._num_hijos) + " soluciones posibles\nDe ellas, se consideran candidatas:\n"

        for i in range(len(self._soluciones_candidatas)):
            str_camino = ''

            for nodo in self._soluciones_candidatas[i].camino():
                if sys.version_info[0] >= 3:
                    str_camino += str(nodo.nombre()) + ' - '

                else:
                    str_camino += nodo.nombre().toPython().encode('utf-8') + ' - '

            texto += SANGRIA + str(i) + ': ' + str_camino[0:-3] + ', con una duración de ' + str(self._soluciones_candidatas[i].duracion()) + " seg.\n"

        del self._soluciones_candidatas

        texto += "El resto se han descartado por no ser válidas\n"

        texto_solucion = ''

        if self.__num_soluciones < len(self._soluciones):
            texto_solucion += "Se ha elegido la solución: \n"

            texto_camino = ''

            for nodo in self._solucion_elegida.camino():
                if sys.version_info[0] >= 3:
                    texto_camino += str(nodo.nombre()) + ' - '

                else:
                    texto_camino += nodo.nombre().toPython().encode('utf-8') + ' - '

            texto_solucion += SANGRIA + texto_camino[0:-3] + ', con una duración de ' + str(self._solucion_elegida.duracion()) + " seg.\n"

        else:
            texto += "\nNo se ha encontrado ninguna otra solución válida\nFin de la ejecución"

        vista.ventana_vista.calcular(self, 'desarrollo', texto + texto_solucion)

        vista.ventana_vista.calcular(self, 'solucion', texto_solucion)

        self._modificado = True


    def closeEvent(self, event):                                                    # Se pregunta al usuario si quiere salir
        respuesta = self.confirmar_modificado('salir')

        if respuesta == vista.respuestas.diccionario[vista.respuestas.DESCARTAR]:
            event.accept()

        elif respuesta == vista.respuestas.diccionario[vista.respuestas.GUARDAR]:
            if self.guardar():
                event.accept()

            else:
                event.ignore()

        else:
            event.ignore()


    def guardado(self):                                                             # Procedimiento de guardado
        try:
            archivo = open(file = self._nombre_archivo, mode = 'w', encoding = 'utf-8')

        except IOError:
            if sys.version_info[0] >= 3:                                            # Llamada al método equivalente de la clase padre
                super().guardado()

            else:
                super(ventana_principal, self).guardado()

            res = False

        else:
            archivo.write(self._text_solucion.toPlainText())

            self.modificado(False)

            res = True

        finally:
            archivo.close()

        return res


    def guardar(self):                                                              # Acción de guardar
        try:
            self._nombre_archivo

        except AttributeError:
            res = self.guardar_como()

        else:
            if self._nombre_archivo == '':
                del self._nombre_archivo

                res = self.guardar_como()

            else:
                res = self.guardado()

        finally:
            pass

        return res


    def guardar_como(self):                                                         # Acción de guardar cómo
        if self._soluciones != []:
            self._nombre_archivo = vista.ventana_vista.guardar_como(self, 'nombre') # Llamada al método equivalente de la clase vista

            if self._nombre_archivo != '':
                return self.guardado()

            else:
                return False

        else:
            vista.ventana_vista.guardar_como(self, 'error')                         # Llamada al método equivalente de la clase vista

            return False


    def imprimir(self):                                                             # Acción de imprimir
        if self._soluciones != []:
            vista.ventana_vista.imprimir(self, 'imprimir')                          # Llamada al método equivalente de la clase vista

        else:
            vista.ventana_vista.imprimir(self, 'error')                             # Llamada al método equivalente de la clase vista

            return False


    def limpiar(self, modo):                                                        # Acción de limpiar
        if modo == 'total':
            self._num_hijos = 1000

            self._prob_heuristica = 50

            self.setWindowTitle(self._TITULO_APP)

            self._slider_heuristica.setValue(self._prob_heuristica)

            self._slider_hijos.setValue(self._num_hijos)

            self._text_ruta.clear()

            self._text_dominio.clear()

            try:
                del self._nombre_archivo

            except AttributeError:
                pass

            try:
                del self._datos

            except AttributeError:
                pass

        self._text_solucion.clear()

        self._text_desarrollo.clear()

        self.modificado(False)

        try:
            del self._grafo

        except AttributeError:
            pass

        self._cronograma = None

        self._soluciones = []

        self.__num_soluciones = 0


    def modificado(self, *args):                                                    # Función "sobrecargada": modificador / observador de la variable self._modificado
        if args != ():
            self._modificado = args[0]

        else:
            pass

        return self._modificado


    def nuevo(self):                                                                # Acción de nuevo
        respuesta = self.confirmar_modificado('cargar un modelo nuevo')

        if respuesta == vista.respuestas.diccionario[vista.respuestas.DESCARTAR]:
            self.limpiar('total')

        elif respuesta == vista.respuestas.diccionario[vista.respuestas.GUARDAR]:
            if self.guardar():
                self.limpiar('total')

            else:
                pass

        else:
            pass


    def __del__(self):                                                              # Constructor de la clase
        if sys.version_info[0] >= 3:                                                # Llamada al método equivalente de la clase padre
            super().__del__()

        else:
            super(ventana_principal, self).__del__()


