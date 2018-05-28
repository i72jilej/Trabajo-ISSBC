#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Title         : vista.py
# Description   : Vista del programa
# Author        : Julio Domingo Jiménez Ledesma
# Author        : Rafael Carlos Méndez Rodríguez
# Date          : 29-05-2018
# Version       : 1.0.0
# Usage         : import vista o from vista import ...
# Notes         : 


TITULO_APP = 'Planificador de cadena de montaje'


import sys                                                              # Funcionalidades varias del sistema

from PyQt4 import QtCore, QtGui

from controlador import ventana_controlador


class ventana_principal(QtGui.QMainWindow, ventana_controlador):
    def __init__(self):                                                 # Constructor de la clase; al ser una ventana, inicializa la misma
        if sys.version_info[0] >= 3:                                    # Llamada al constructor de la clase padre
            super().__init__()
        else:
            super(ventana_principal, self).__init__()

        self.setWindowIcon(QtGui.QIcon('./iconos/000-checklist.png'))   # Establecer el icono de la ventana principal

        self._widget_principal = QtGui.QWidget(self)                    # Establecer el widget principal

        self.setCentralWidget(self._widget_principal)                   # Establecer el widget central

        self.dibujar_interfaz()                                         # Dibujar la interfaz

        self._widget_principal.setLayout(self._disenyo)                 # Establecer el diseño del widget

        self.crearAcciones()                                            # Crer los menús, barras de herramientas y acciones que éstos dispararán
                                                                        # Es importante crear las acciones lo primero, ya que el resto de elementos dependen de ellas
        self.crearMenus()

        self.crearBarraDeHerramientas()

        self.statusBar().showMessage('Esperando archivo')               # Se establece el mensaje para barra de estado

        self.setWindowTitle(TITULO_APP)                                 # Se establece el título de la ventana

        self.setMinimumSize(640, 480)                                   # Parámetros de tamaño

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


    def crearAcciones(self):                                	       	# Se crean las acciones asociadas al menú y a la barra de herramientas
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


    def crearBarraDeHerramientas(self):                     	        # Se crea la barra de herramientas
        self._toolbar = self.addToolBar('Barra de herramientas')
        self._toolbar.addAction(self.nuevoAcc)
        self._toolbar.addAction(self.abrirAcc)
        self._toolbar.addAction(self.guardarAcc)
        self._toolbar.addAction(self.guardarComoAcc)
        self._toolbar.addSeparator()
        self._toolbar.addAction(self.calcularAcc)
        self._toolbar.addSeparator()
        self._toolbar.addAction(self.salirAcc)

        self._toolbar.setMovable(False)                                 # Hace la barra inamovible


    def crearMenus(self):                                   	        # Se crean los menús
        self._menu_archivo = self.menuBar().addMenu('&Archivo')
        self._menu_archivo.addAction(self.nuevoAcc)
        self._menu_archivo.addAction(self.abrirAcc)
        self._menu_archivo.addAction(self.guardarAcc)
        self._menu_archivo.addAction(self.guardarComoAcc)
        self._menu_archivo.addSeparator()
        self._menu_archivo.addAction(self.imprimirAcc)
        self._menu_archivo.addSeparator()
        self._menu_archivo.addAction(self.salirAcc)

        if sys.version_info[0] >= 3:
            self._menu_accion = self.menuBar().addMenu('A&cción')
        else:
            self._menu_accion = self.menuBar().addMenu(u'A&cción')

        self._menu_accion.addAction(self.calcularAcc)

        self._menu_ayuda = self.menuBar().addMenu("A&yuda")
        self._menu_ayuda.addAction(self.acercaDeAcc)
        self._menu_ayuda.addAction(self.acercaDeQtAcc)


    def dibujar_interfaz(self):
        self._disenyo = QtGui.QVBoxLayout()
        self._disenyo.addWidget(self.dibujar_mitad_superior())
        self._disenyo.addWidget(self.dibujar_mitad_inferior())


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

        # Diseño
        disenyo = QtGui.QVBoxLayout()
        disenyo.addWidget(label_solucion)
        disenyo.addWidget(self._text_solucion)
        disenyo.addWidget(label_desarrollo)
        disenyo.addWidget(self._text_desarrollo)
        disenyo.addWidget(label_dominio)
        disenyo.addWidget(self._text_dominio)

        # Widget
        mitad_inferior = QtGui.QGroupBox('Resultados')
        mitad_inferior.setLayout(disenyo)

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

        # Diseño
        disenyo = QtGui.QHBoxLayout()
        disenyo.addWidget(label_archivo)
        disenyo.addWidget(self._text_ruta)
        disenyo.addWidget(self._boton_abrir)

        # Widget
        mitad_superior = QtGui.QGroupBox('Carga del archivo')
        mitad_superior.setLayout(disenyo)

        return mitad_superior


