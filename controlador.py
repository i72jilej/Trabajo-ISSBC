#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Title         : controlador.py
# Description   : Controlador del programa
# Author        : Julio Domingo Jiménez Ledesma
# Author        : Rafael Carlos Méndez Rodríguez
# Date          : 30-05-2018
# Version       : 1.0.0
# Usage         : import controlador o from controlador import ...
# Notes         : 


SANGRIA = '        '


import sys                                                      # Funcionalidades varias del sistema

import modelo                                                   # Modelo del programa
import vista                                                    # Vista del programa

if sys.version_info[0] < 3:
    from io import open


class ventana_principal(modelo.ventana_modelo, vista.ventana_vista):
    _modificado = False                                         # Inicialización de variables de clase
    _n_hilos = 1000                                             # Número de hilos a utilizar (soluciones posibles)


    def __init__(self):                                         # Constructor de la clase
        if sys.version_info[0] >= 3:                            # Llamada al método equivalente de la clase padre
            super().__init__()

        else:
            super(ventana_principal, self).__init__()

        self._cronograma = None

        self._soluciones = []


    def abrir(self):                                            # Acción de abrir
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


    def apertura(self):                                         # Procedimiento de apertura
        textos = [
                    ' es una máquina con duración ',
                    ' con una duración de '
                 ]

        if sys.version_info[0] >= 3:                            # Llamada al método equivalente de la clase padre
            nombre_archivo = super().apertura('abrir')

        else:
            nombre_archivo = super(ventana_principal, self).apertura('abrir')

            for texto in textos:
                texto = texto.decode('utf-8')

        if nombre_archivo != '':                                # Comprobando si se ha elegido algún archivo
            # try:                                                # Si se ha elegido un archivo
            archivo = open(file = nombre_archivo, mode = 'r', encoding = 'utf-8')

            # except IOError:
            #     res = False

            # else:
            texto_archivo = archivo.read()

            self.modificado(False)

            grafo = self.procesar(texto_archivo)

            if grafo != None:
                self._datos = self.interpretar(grafo)       # Extrayendo datos manejables del grafo

                texto_archivo = ''                          # Necesario para reutilizar la dichosa variable

                for i in range(len(self._datos)):           # Construyendo la descripción del dominio
                    if sys.version_info[0] >= 3:
                        texto_archivo += self._datos[i].nombre() + textos[0] + str(self._datos[i].duracion()) + "\n"

                    else:
                        texto_archivo += self._datos[i].nombre()
                        texto_archivo += textos[0]
                        texto_archivo += str(self._datos[i].duracion())
                        texto_archivo += "\n"

                    for padre in self._datos[i].padres():
                        if sys.version_info[0] >= 3:
                            texto_archivo += SANGRIA + 'Requiere haber pasado por ' + padre.nombre() + '\n'

                        else:
                            texto_archivo += SANGRIA + 'Requiere haber pasado por '
                            texto_archivo += padre.nombre()
                            texto_archivo += '\n'

                    for conexion in self._datos[i].conexiones():
                        if sys.version_info[0] >= 3:
                            texto_archivo += SANGRIA + 'Puede enviar a ' + conexion['objeto'].nombre() + texto[3] + str(conexion['duracion']) + '\n'

                        else:
                            texto_archivo += SANGRIA + 'Puede enviar a '
                            texto_archivo += conexion['objeto'].nombre()
                            texto_archivo += textos[1]
                            texto_archivo += str(conexion['duracion'])
                            texto_archivo += '\n'

                    texto_archivo += '\n'

                if sys.version_info[0] >= 3:                # Llamada al método equivalente de la clase padre
                    super().apertura('dominio', texto_archivo, nombre_archivo)

                else:
                    super(ventana_principal, self).apertura('dominio', texto_archivo.decode('utf-8'), nombre_archivo)

                res = True

            else:
                if sys.version_info[0] >= 3:                # Llamada al método equivalente de la clase padre
                    nombre_archivo = super().apertura('error')

                else:
                    nombre_archivo = super(ventana_principal, self).apertura('error')

                self.limpiar()

                return False

            # finally:
            try:
                archivo.close()

            except UnboundLocalError:
                pass

            return res


    def calcular(self):                                         # Realiza los cálculos necesarios
        try:
            self._datos

        except AttributeError:
            vista.ventana_vista.calcular(self, 'error')         # Llamada al método equivalente de la clase vista

        else:
            if self._soluciones != []:
                respuesta = self.confirmar_modificado('realizar nuevos cálculos')

                if respuesta == vista.respuestas.diccionario[vista.respuestas.DESCARTAR]:
                    self.limpiar('parcial')

                    self.calculo()

                elif respuesta == vista.respuestas.diccionario[vista.respuestas.GUARDAR]:
                    if self.guardar():
                        self.limpiar('parcial')

                        self.calculo()

                    else:
                        pass

                else:
                    pass

            else:
                self.calculo()

        finally:
            pass


    def calculo(self):                                          # Acción de realizar los cálculos
        modelo.ventana_modelo.calcular(self, self._n_hilos) # Llamada al método equivalente de la clase vista

        texto = 'Se han generado ' + str(self._n_hilos) + " soluciones posibles\nDe ellas, se consideran candidatas:\n"

        i = 0

        for solucion in self._soluciones_candidatas:
            str_camino = ''
            tiempo = solucion.duracion()

            for nodo in solucion.camino():
                str_camino += nodo.nombre() + ' - '

            i += 1

            texto = texto + SANGRIA + str(i) + ': ' + str_camino[0:-3] + ' con una duración de ' + str(tiempo) + " seg.\n"

        vista.ventana_vista.calcular(self, 'desarrollo', texto)

        del self._soluciones_candidatas

        self._modificado = True


    def closeEvent(self, event):                                # Se pregunta al usuario si quiere salir
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


    def guardado(self):                                         # Procedimiento de guardado
        try:
            archivo = open(file = self._nombre_archivo, mode = 'w', encoding = 'utf-8')

        except IOError:
            if sys.version_info[0] >= 3:                        # Llamada al método equivalente de la clase padre
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


    def guardar(self):                                          # Acción de guardar
        try:
            self._nombre_archivo

        except AttributeError:
            return self.guardar_como()

        else:
            if self._nombre_archivo == '':
                del self._nombre_archivo

                return self.guardar_como()

            else:
                return self.guardado()

        finally:
            pass

        return True


    def guardar_como(self):                                     # Acción de guardar cómo
        if sys.version_info[0] >= 3:                            # Llamada al método equivalente de la clase padre
            self._nombre_archivo = super().guardar_como()

        else:
            self._nombre_archivo = super(ventana_principal, self).guardar_como()

        if self._nombre_archivo != '':
            return self.guardado()

        else:
            return False


    def limpiar(self, modo):                                    # Acción de limpiar
        if modo == 'total':
            self._text_ruta.clear()

            self._text_dominio.clear()

            self.setWindowTitle(self._TITULO_APP)

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


    def modificado(self, *args):                                # Función "sobrecargada": modificador / observador de la variable self._modificado
        if args != ():
            self._modificado = args[0]

        else:
            pass

        return self._modificado


    def nuevo(self):                                            # Acción de nuevo
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


    def __del__(self):                                          # Constructor de la clase
        if sys.version_info[0] >= 3:                            # Llamada al método equivalente de la clase padre
            super().__del__()

        else:
            super(ventana_principal, self).__del__()


