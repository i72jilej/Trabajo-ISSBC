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


import sys                                                  # Funcionalidades varias del sistema

from PyQt4 import QtCore, QtGui

from controlador import ventana_controlador


TITULO_APP = 'Planificador de cadena de montaje'


class ventana_principal(QtGui.QMainWindow, ventana_controlador):
    def __init__(self):                                     # Constructor de la clase; al ser una ventana, inicializa la misma
        if sys.version_info[0] >= 3:                        # Llamada al constructor de la clase padre
            super().__init__()
        else:
            super(ventana_principal, self).__init__()

        self.setWindowIcon(QtGui.QIcon('./iconos/000-checklist.png'))

        self.widgetCentral = QtGui.QWidget(self)

        self.setCentralWidget(self.widgetCentral)           # Establecer el widget central

        self.dibujar_interfaz()

        self.widgetCentral.setLayout(self._layout)

        self.crearAcciones()                                # Crer los menús, barras de herramientas y acciones que éstos dispararán
                                                            # Es importante crear las acciones lo primero, ya que el resto de elementos dependen de ellas
        self.crearMenus()

        self.crearBarraDeHerramientas()

        if sys.version_info[0] >= 3:                        # Se establece la barra de estado, invocando al método correspondiente directamente
            self.statusBar().showMessage('Listo y esperando órdenes')
        else:
            self.statusBar().showMessage(u'Listo y esperando órdenes')

        self.setWindowTitle(TITULO_APP)                     # Se establece el título de la ventana

        self.setMinimumSize(640, 480)                       # Parámetros de tamaño

        self.resize(800, 600)


    def acercaDe(self):
        acerca_de = QtGui.QMessageBox()
        acerca_de.setWindowTitle('Acerca de')
        acerca_de.setTextFormat(QtCore.Qt.RichText)

        if sys.version_info[0] >= 3:
            acerca_de.setText('''<p>Trabajo de planificación creada por Julio Domingo Jiménez Ledesma (i72jilej) y Rafael Carlos Méndez Rodríguez (i82meror)</p>
<p>Icono usado en "Nuevo" por <a href="https://www.flaticon.com/authors/yannick">Yannick</a><br />
Icono usado en "Abrir" por <a href="https://www.flaticon.com/authors/simpleicon">SimpleIcon</a><br />
Iconos usados en la ventana principal, "Guardar", "Calcular", "Acerca de" y "Acerca de Qt" por <a href="https://www.flaticon.com/authors/freepik">Freepic</a><br />
Iconos usados en "Guardar como" y "Salir" por <a href="https://www.flaticon.com/authors/smashicons">Smashicons</a><br />
Icono usado en "Imprimir" por <a href="https://www.flaticon.com/authors/dave-gandy">Dave Gandy</a><br />
Todos ellos autores de <a href="https://www.flaticon.com/">www.flaticon.com</a></p>
''')
        else:
            acerca_de.setText(u'''<p>Trabajo de planificación creada por Julio Domingo Jiménez Ledesma (i72jilej) y Rafael Carlos Méndez Rodríguez (i82meror)</p>
<p>Icono usado en "Nuevo" por <a href="https://www.flaticon.com/authors/yannick">Yannick</a><br />
Icono usado en "Abrir" por <a href="https://www.flaticon.com/authors/simpleicon">SimpleIcon</a><br />
Iconos usados en la ventana principal, "Guardar", "Calcular", "Acerca de" y "Acerca de Qt" por <a href="https://www.flaticon.com/authors/freepik">Freepic</a><br />
Iconos usados en "Guardar como" y "Salir" por <a href="https://www.flaticon.com/authors/smashicons">Smashicons</a><br />
Icono usado en "Imprimir" por <a href="https://www.flaticon.com/authors/dave-gandy">Dave Gandy</a><br />
Todos ellos autores de <a href="https://www.flaticon.com/">www.flaticon.com</a></p>
''')

        acerca_de.exec()


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

        self.calcularAcc        = QtGui.QAction("&Calcular",        self, shortcut = 'F4',                      statusTip = 'Comienza los cálculos',                                triggered = self.calcular       )
        self.acercaDeAcc        = QtGui.QAction("&Acerca de",       self, shortcut = 'F1',                      statusTip = 'Muestra la ventana "Acerca de"',                       triggered = self.acercaDe       )

        if sys.version_info[0] >= 3:
            self.acercaDeQtAcc  = QtGui.QAction("Acerca de &Qt",    self,                                       statusTip = 'Muestra la ventana "Acerca de" de la librería Qt',     triggered = self.acercaDeQt     )
        else:
            self.acercaDeQtAcc  = QtGui.QAction("Acerca de &Qt",    self,                                       statusTip = u'Muestra la ventana "Acerca de" de la librería Qt',    triggered = self.acercaDeQt     )

        self.acercaDeQtAcc.triggered.connect(QtGui.qApp.aboutQt)

        self.nuevoAcc.          setIcon(QtGui.QIcon('./iconos/001-add-new-document.png')                            )
        self.abrirAcc.          setIcon(QtGui.QIcon('./iconos/002-folder-black-open-shape.png')                     )
        self.guardarAcc.        setIcon(QtGui.QIcon('./iconos/003-save-icon.png')                                   )
        self.guardarComoAcc.    setIcon(QtGui.QIcon('./iconos/004-technology.png')                                  )
        self.imprimirAcc.       setIcon(QtGui.QIcon('./iconos/005-printing-tool.png')                               )
        self.salirAcc.          setIcon(QtGui.QIcon('./iconos/006-logout.png')                                      )
        self.calcularAcc.       setIcon(QtGui.QIcon('./iconos/007-calculator.png')                                  )
        self.acercaDeAcc.       setIcon(QtGui.QIcon('./iconos/008-about-us.png')                                    )
        self.acercaDeQtAcc.     setIcon(QtGui.QIcon('./iconos/009-presenter-talking-about-people-on-a-screen.png')  )


    def crearBarraDeHerramientas(self):                     # Se crea la barra de herramientas
        self.toolbar = self.addToolBar('Barra de herramientas')
        self.toolbar.addAction(self.nuevoAcc)
        self.toolbar.addAction(self.abrirAcc)
        self.toolbar.addAction(self.guardarAcc)
        self.toolbar.addAction(self.guardarComoAcc)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.calcularAcc)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.salirAcc)

        self.toolbar.setMovable(False)                      # Hace la barra inamovible


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

        if sys.version_info[0] >= 3:
            self.menuAccion = self.menuBar().addMenu('A&cción')
        else:
            self.menuAccion = self.menuBar().addMenu(u'A&cción')

        self.menuAccion.addAction(self.calcularAcc)

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


    def dibujar_interfaz(self):
        mitad_inferior = self.dibujar_mitad_inferior()

        mitad_superior = self.dibujar_mitad_superior()
        
        self._layout = QtGui.QVBoxLayout()
        self._layout.addWidget(mitad_inferior)
        self._layout.addWidget(mitad_superior)


    def dibujar_mitad_inferior(self):
        # Etiquetas
        label_desarrollo = QtGui.QLabel('Desarrollo:')

        label_dominio = QtGui.QLabel('Dominio:')

        if sys.version_info[0] >= 3:
            label_solucion = QtGui.QLabel('Solución:')
        else:
            label_solucion = QtGui.QLabel(u'Solución:')

        # Controles de edición
        self._text_desarrollo = QtGui.QTextEdit()
        self._text_desarrollo.setReadOnly(True)

        self._text_dominio = QtGui.QTextEdit()
        self._text_dominio.setReadOnly(True)

        self._text_solucion = QtGui.QTextEdit()
        self._text_solucion.setReadOnly(True)

        # Layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label_solucion)
        layout.addWidget(self._text_solucion)
        layout.addWidget(label_desarrollo)
        layout.addWidget(self._text_desarrollo)
        layout.addWidget(label_dominio)
        layout.addWidget(self._text_dominio)

        # Widget
        mitad_inferior = QtGui.QGroupBox('Resultados')
        mitad_inferior.setLayout(layout)

        return mitad_inferior


    def dibujar_mitad_superior(self):
        # Botones
        self._boton_abrir = QtGui.QPushButton('Abrir')
        self._boton_abrir.clicked.connect(self.abrir)
        self._boton_abrir.setMaximumWidth(84)

        # Controles de edición
        self._text_ruta = QtGui.QLineEdit()
        self._text_ruta.setReadOnly(True)

        # Etiquetas
        label_archivo = QtGui.QLabel('Archivo:')
        label_archivo.setMaximumWidth(42)

        # Layout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(label_archivo)
        layout.addWidget(self._text_ruta)
        layout.addWidget(self._boton_abrir)

        # Widget
        mitad_superior = QtGui.QGroupBox('Carga del archivo')
        mitad_superior.setLayout(layout)

        return mitad_superior


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

