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


import sys                                                  # Funcionalidades varias del sistema

from PyQt4 import QtGui

from vista import ventana_compositor


TITULO_APP = 'Planificador de cadena de montaje'


class ventana_principal(QtGui.QMainWindow, ventana_compositor):
    # Inicialización de variables de clase
    _modificado = False

    def __init__(self):                                     # Constructor de la clase; al ser una ventana, inicializa la misma
        if sys.version_info[0] >= 3:                        # Llamada al constructor de la clase padre
            super().__init__()
        else:
            super(ventana_principal, self).__init__()

        # TODO: self.setCentralWidget(self.textEdit)                # Establecer el widget central

        self.crearAcciones()                                # Crer los menús, barras de herramientas y acciones que éstos dispararán
                                                            # Es importante crear las acciones lo primero, ya que el resto de elementos dependen de ellas
        self.crearMenus()

        if sys.version_info[0] >= 3:                        # Se establece la barra de estado, invocando al método correspondiente directamente
            self.statusBar().showMessage('Listo y esperando órdenes')
        else:
            self.statusBar().showMessage(u'Listo y esperando órdenes')

        self.setWindowTitle(TITULO_APP)                     # Se establece el título de la ventana

        self.setMinimumSize(160, 160)                       # Parámetros de tamaño
        self.resize(480, 320)


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

    
    def acercaDe(self):
        if sys.version_info[0] >= 3:
            QtGui.QMessageBox.about(self, 'Acerca de', 'Trabajo de planificación creada por Julio Domingo Jiménez Ledesma (i72jilej) y Rafael Carlos Méndez Rodríguez (i82meror)')
        else:
            QtGui.QMessageBox.about(self, 'Acerca de', u'Trabajo de planificación creada por Julio Domingo Jiménez Ledesma (i72jilej) y Rafael Carlos Méndez Rodríguez (i82meror)')


    def acercaDeQt(self):
        pass


    def apertura(self):
        self._nombre_archivo = QtGui.QFileDialog.getOpenFileName(self, 'Abrir archivo', filter = 'Documentos de texto (*.txt);;Todos los archivos (*.*)')

        try:
            if self._nombre_archivo != '':
                try:
                    archivo = open(file = self._nombre_archivo, mode = 'r', encoding = 'utf-8')

                except IOError:
                    QtGui.QMessageBox.warning(self, 'Error de apertura', 'Error: Archivo <' + self._nombre_archivo + '> inaccesible')

                else:
                    texto = archivo.read()

                    # FIXME: Así no self.textEdit.setText(texto)

                    self.modificado(False)

                    self.setWindowTitle(TITULO_APP + ': ' + self._nombre_archivo)

                finally:
                    try:
                        archivo.close()

                    except UnboundLocalError:
                        pass

                    return True

        except AttributeError:
            return False


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


    def crearAcciones(self):                                # Se crean las acciones asociadas al menú y a la barra de herramientas
        self.nuevoAcc           = QtGui.QAction('&Nuevo',           self, shortcut = QtGui.QKeySequence.New,    statusTip = 'Crea un nuevo archivo',                                triggered = self.nuevo          )
        self.abrirAcc           = QtGui.QAction('&Abrir...',        self, shortcut = QtGui.QKeySequence.Open,   statusTip = 'Abre un archivo existente',                            triggered = self.abrir          )
        self.guardarAcc         = QtGui.QAction('&Guardar',         self, shortcut = QtGui.QKeySequence.Save,   statusTip = 'Guarda el archivo',                                    triggered = self.guardar        )
        self.guardarComoAcc     = QtGui.QAction('Guardar c&omo',    self, shortcut = QtGui.QKeySequence.SaveAs, statusTip = 'Guarda el archivo con un nombre distinto',             triggered = self.guardarComo    )
        self.imprimirAcc        = QtGui.QAction('Im&primir',        self, shortcut = QtGui.QKeySequence.Print,  statusTip = 'Imprime el archivo',                                   triggered = self.imprimir       )
        if sys.version_info[0] >= 3:
            self.salirAcc       = QtGui.QAction('&Salir',           self, shortcut = 'Alt+F4',                  statusTip = 'Sale de la aplicación',                                triggered = self.close          )
        else:
            self.salirAcc       = QtGui.QAction('&Salir',           self, shortcut = 'Alt+F4',                  statusTip = u'Sale de la aplicación',                               triggered = self.close          )

        self.acercaDeAcc        = QtGui.QAction("&Acerca de",       self,                                       statusTip = 'Muestra la ventana "Acerca de"',                       triggered = self.acercaDe       )
        if sys.version_info[0] >= 3:
            self.acercaDeQtAcc  = QtGui.QAction("Acerca de &Qt",    self,                                       statusTip = 'Muestra la ventana "Acerca de" de la librería Qt',     triggered = self.acercaDeQt     )
        else:
            self.acercaDeQtAcc  = QtGui.QAction("Acerca de &Qt",    self,                                       statusTip = u'Muestra la ventana "Acerca de" de la librería Qt',    triggered = self.acercaDeQt     )

        self.acercaDeQtAcc.triggered.connect(QtGui.qApp.aboutQt)


    def crearMenus(self):                                   # Se crean los menús
        self.menuArchivo = self.menuBar().addMenu('&Archivo')
        self.menuArchivo.addAction(self.nuevoAcc)
        self.menuArchivo.addAction(self.abrirAcc)
        self.menuArchivo.addAction(self.guardarAcc)
        self.menuArchivo.addAction(self.guardarComoAcc)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.imprimirAcc)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.salirAcc)

        self.menuAyuda = self.menuBar().addMenu("A&yuda")
        self.menuAyuda.addAction(self.acercaDeAcc)
        self.menuAyuda.addAction(self.acercaDeQtAcc)


    def confirmarModificado(self):
        # TODO: Ponerle nombre a los botones

        if self.modificado():
            if sys.version_info[0] >= 3:
                return QtGui.QMessageBox.question(self, 'Aviso', 'El archivo ha sido modificado. ¿Desea guardarlo antes de salir?', QtGui.QMessageBox.Discard | QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)
            else:
                return QtGui.QMessageBox.question(self, 'Aviso', u'El archivo ha sido modificado. ¿Desea guardarlo antes de salir?', QtGui.QMessageBox.Discard | QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)
        else:
            return True


    def guardado(self):
        try:
            archivo = open(file = self._nombre_archivo, mode = 'w', encoding = 'utf-8')

        except IOError:
            QtGui.QMessageBox.warning(self, 'Error de apertura', 'Error: Archivo <' + self._nombre_archivo + '> inaccesible')

            return False


        else:
            # FIXME: Así tampoco archivo.write(self.textEdit.toPlainText())

            self.setWindowTitle(TITULO_APP + ': ' + self._nombre_archivo)

            self.modificado(False)

            return True

        finally:
            archivo.close()


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


    def modificado(self, *args):
        if args != ():
            self._modificado = args[0]

            return True
        else:
            return self._modificado


    def nuevo(self):                                        # Acción de nuevo
        respuesta = self.confirmarModificado()

        if respuesta == QtGui.QMessageBox.Discard or respuesta == True:
            self.textEdit.clear()

            self.modificado(False)

            self.setWindowTitle(TITULO_APP)

            try:
                del self._nombre_archivo

            except AttributeError:
                pass

        elif respuesta == QtGui.QMessageBox.Save:
            if self.guardar():
                self.textEdit.clear()

                self.setWindowTitle(TITULO_APP)

                del self._nombre_archivo

            else:
                pass

        else:
            pass


