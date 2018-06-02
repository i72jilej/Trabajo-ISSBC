#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Title         : vista.py
# Description   : Vista del programa
# Author        : Julio Domingo Jiménez Ledesma
# Author        : Rafael Carlos Méndez Rodríguez
# Date          : 30-05-2018
# Version       : 1.0.0
# Usage         : import vista o from vista import ...
# Notes         : 


import sys                                                              # Funcionalidades varias del sistema

from PyQt4 import QtGui                                                 # Módulo de interfaz de usuario de PyQt4


class respuestas():
    DESCARTAR               = 0
    CANCELAR                = 1
    GUARDAR                 = 2

    diccionario             = []
    diccionario.append(QtGui.QMessageBox.Discard)
    diccionario.append(QtGui.QMessageBox.Cancel)
    diccionario.append(QtGui.QMessageBox.Save)


class ventana_vista(QtGui.QMainWindow):                                 # Parte de la vista de la ventana
    _TITULO_APP = 'Planificador de cadena de montaje'


    def __init__(self):                                                 # Parte de la vista del constructor de la clase; al ser una ventana, inicializa la misma
        if sys.version_info[0] >= 3:                                    # Llamada al constructor de la clase padre
            super().__init__()
        else:
            super(ventana_vista, self).__init__()

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

        self.setWindowTitle(self._TITULO_APP)                           # Se establece el título de la ventana

        self.setMinimumSize(640, 480)                                   # Parámetros de tamaño

        self.resize(800, 600)


    def acercaDe(self):                                                 # Ventana modal que muestra la información de "Acerca de"
        texto = '''<p>Trabajo de planificación creada por Julio Domingo Jiménez Ledesma (i72jilej) y Rafael Carlos Méndez Rodríguez (i82meror)</p>
<p>Icono usado en "Nuevo" por <a href="https://www.flaticon.com/authors/yannick">Yannick</a><br />
Icono usado en "Abrir" por <a href="https://www.flaticon.com/authors/simpleicon">SimpleIcon</a><br />
Iconos usados en la ventana principal, "Guardar", "Calcular", "Acerca de" y "Acerca de Qt" por <a href="https://www.flaticon.com/authors/freepik">Freepic</a><br />
Iconos usados en "Guardar como" y "Salir" por <a href="https://www.flaticon.com/authors/smashicons">Smashicons</a><br />
Icono usado en "Imprimir" por <a href="https://www.flaticon.com/authors/dave-gandy">Dave Gandy</a><br />
Todos ellos autores de <a href="https://www.flaticon.com/">www.flaticon.com</a></p>
'''

        if sys.version_info[0] < 3:
            texto = texto.decode('utf-8')

        QtGui.QMessageBox.about(self, 'Acerca de', texto)


    def acercaDeQt(self):                                               # Ventana modal que muestra la información de "Acerca de Qt"
        QtGui.qApp.aboutQt()


    def apertura(self, modo, *args):                                    # Parte de la vista del procedimiento de apertura
        if modo == 'abrir':
            return str(QtGui.QFileDialog.getOpenFileName(self, 'Abrir archivo', filter = 'Base de conocimiento NTriples (*.nt);;Todos los archivos (*.*)'))

        elif modo == 'error':
            return QtGui.QMessageBox.warning(self, 'Aviso', 'El formato del archivo es incorrecto o no ha podido ser cargado')

        elif modo == 'dominio':
            self._text_dominio.setText(args[0])

            return True


    def calcular(self):                                                 # Parte de la vista de la realización de los cálculos necesarios
        texto = 'Error de cálculo'

        if sys.version_info[0] < 3:
            texto = texto.decode('utf-8')

        QtGui.QMessageBox.warning(self, texto, 'Aviso: No se ha cargado ningún archivo')


    def confirmar_modificado(self, accion):                             # Confirmación de las modificaciones antes de realizar una operación que pueda destruirlas
        if self.modificado():
            texto = 'Hay cálculos no guardados. ¿Desea guardarlos antes de ' + accion + '?'
    
            if sys.version_info[0] < 3:
                texto = texto.decode('utf-8')

            mensaje = QtGui.QMessageBox()
            mensaje.setIcon(QtGui.QMessageBox.Question)
            mensaje.setWindowTitle('Aviso')
            mensaje.setText(texto)
            mensaje.setStandardButtons(QtGui.QMessageBox.Discard | QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel)
            mensaje.setDefaultButton(QtGui.QMessageBox.Cancel)

            boton_descartar = mensaje.button(QtGui.QMessageBox.Discard)
            boton_descartar.setText('Descartar')

            boton_guardar = mensaje.button(QtGui.QMessageBox.Save)
            boton_guardar.setText('Guardar')

            boton_cancelar = mensaje.button(QtGui.QMessageBox.Cancel)
            boton_cancelar.setText('Cancelar')

            return mensaje.exec_()

            # return QtGui.QMessageBox.question(self, 'Aviso', texto, QtGui.QMessageBox.Discard | QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

        else:
            return QtGui.QMessageBox.Discard


    def crearAcciones(self):                                	       	# Creación de las acciones asociadas al menú y a la barra de herramientas
        textos = []
        textos.append('Sale de la aplicación')
        textos.append('Muestra la ventana "Acerca de" de la librería Qt')

        if sys.version_info[0] < 3:
            for texto in textos:
                texto = texto.decode('utf-8')

        self.nuevoAcc           = QtGui.QAction('&Nuevo',           self, shortcut = QtGui.QKeySequence.New,    statusTip = 'Crea un nuevo archivo',                                triggered = self.nuevo          )
        self.abrirAcc           = QtGui.QAction('&Abrir...',        self, shortcut = QtGui.QKeySequence.Open,   statusTip = 'Abre un archivo existente',                            triggered = self.abrir          )
        self.guardarAcc         = QtGui.QAction('&Guardar',         self, shortcut = QtGui.QKeySequence.Save,   statusTip = 'Guarda el archivo',                                    triggered = self.guardar        )
        self.guardarComoAcc     = QtGui.QAction('Guardar c&omo',    self, shortcut = QtGui.QKeySequence.SaveAs, statusTip = 'Guarda el archivo con un nombre distinto',             triggered = self.guardar_como   )
        self.imprimirAcc        = QtGui.QAction('Im&primir',        self, shortcut = QtGui.QKeySequence.Print,  statusTip = 'Imprime el archivo',                                   triggered = self.imprimir       )
        self.salirAcc           = QtGui.QAction('&Salir',           self, shortcut = 'Alt+F4',                  statusTip = textos[0],                                              triggered = self.close          )
        self.calcularAcc        = QtGui.QAction('&Calcular',        self, shortcut = 'F4',                      statusTip = 'Comienza los cálculos',                                triggered = self.calcular       )
        self.acercaDeAcc        = QtGui.QAction('&Acerca de',       self, shortcut = 'F1',                      statusTip = 'Muestra la ventana "Acerca de"',                       triggered = self.acercaDe       )
        self.acercaDeQtAcc      = QtGui.QAction('Acerca de &Qt',    self,                                       statusTip = textos[1],                                              triggered = self.acercaDeQt     )

        self.nuevoAcc.          setIcon(QtGui.QIcon('./iconos/001-add-new-document.png')                            )
        self.abrirAcc.          setIcon(QtGui.QIcon('./iconos/002-folder-black-open-shape.png')                     )
        self.guardarAcc.        setIcon(QtGui.QIcon('./iconos/003-save-icon.png')                                   )
        self.guardarComoAcc.    setIcon(QtGui.QIcon('./iconos/004-technology.png')                                  )
        self.imprimirAcc.       setIcon(QtGui.QIcon('./iconos/005-printing-tool.png')                               )
        self.salirAcc.          setIcon(QtGui.QIcon('./iconos/006-logout.png')                                      )
        self.calcularAcc.       setIcon(QtGui.QIcon('./iconos/007-calculator.png')                                  )
        self.acercaDeAcc.       setIcon(QtGui.QIcon('./iconos/008-about-us.png')                                    )
        self.acercaDeQtAcc.     setIcon(QtGui.QIcon('./iconos/009-presenter-talking-about-people-on-a-screen.png')  )


    def crearBarraDeHerramientas(self):                     	        # Creación de la barra de herramientas
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


    def crearMenus(self):                                   	        # Creación de los menús
        texto = 'A&cción'

        if sys.version_info[0] < 3:
            texto = texto.decode('utf-8')

        self._menu_archivo = self.menuBar().addMenu('&Archivo')
        self._menu_archivo.addAction(self.nuevoAcc)
        self._menu_archivo.addAction(self.abrirAcc)
        self._menu_archivo.addAction(self.guardarAcc)
        self._menu_archivo.addAction(self.guardarComoAcc)
        self._menu_archivo.addSeparator()
        self._menu_archivo.addAction(self.imprimirAcc)
        self._menu_archivo.addSeparator()
        self._menu_archivo.addAction(self.salirAcc)

        self._menu_accion = self.menuBar().addMenu(texto)
        self._menu_accion.addAction(self.calcularAcc)

        self._menu_ayuda = self.menuBar().addMenu("A&yuda")
        self._menu_ayuda.addAction(self.acercaDeAcc)
        self._menu_ayuda.addAction(self.acercaDeQtAcc)


    def dibujar_interfaz(self):                                         # Dibujo de la interfaz
        self._disenyo = QtGui.QVBoxLayout()                             # Establecimiento del tipo de interfaz
        self._disenyo.addWidget(self.dibujar_intarfaz_mitad_superior()) # Añadiendo widgets a base de funciones externas
        self._disenyo.addWidget(self.dibujar_intarfaz_mitad_inferior())


    def dibujar_intarfaz_mitad_inferior(self):                          # Dibujo de la mitad inferior de la interfaz
        # Diseño
        disenyo = QtGui.QHBoxLayout()
        disenyo.addWidget(self.dibujar_interfaz_mitad_inferior_dominio())
        disenyo.addWidget(self.dibujar_interfaz_mitad_inferior_solucion())
        disenyo.addWidget(self.dibujar_interfaz_mitad_inferior_desarrollo())

        # Widget
        mitad_inferior = QtGui.QGroupBox('Resultados')
        mitad_inferior.setLayout(disenyo)

        return mitad_inferior


    def dibujar_interfaz_mitad_inferior_desarrollo(self):
        # Etiquetas
        label_desarrollo = QtGui.QLabel('Desarrollo:')

        # Controles de edición
        self._text_desarrollo = QtGui.QTextEdit()
        self._text_desarrollo.setReadOnly(True)

        # Diseño
        disenyo = QtGui.QVBoxLayout()
        disenyo.addWidget(label_desarrollo)
        disenyo.addWidget(self._text_desarrollo)

        # Widget
        desarrollo = QtGui.QGroupBox()
        desarrollo.setLayout(disenyo)

        return desarrollo


    def dibujar_interfaz_mitad_inferior_dominio(self):
        # Etiquetas
        label_dominio = QtGui.QLabel('Dominio:')

        # Controles de edición
        self._text_dominio = QtGui.QTextEdit()
        self._text_dominio.setReadOnly(True)

        # Diseño
        disenyo = QtGui.QVBoxLayout()
        disenyo.addWidget(label_dominio)
        disenyo.addWidget(self._text_dominio)

        # Widget
        dominio = QtGui.QGroupBox()
        dominio.setLayout(disenyo)

        return dominio


    def dibujar_interfaz_mitad_inferior_solucion(self):
        texto = 'Solución:'

        if sys.version_info[0] < 3:
            texto = texto.decode('utf-8')

        # Etiquetas
        label_solucion = QtGui.QLabel(texto)

        # Controles de edición
        self._text_solucion = QtGui.QTextEdit()
        self._text_solucion.setReadOnly(True)

        # Diseño
        disenyo = QtGui.QVBoxLayout()
        disenyo.addWidget(label_solucion)
        disenyo.addWidget(self._text_solucion)

        # Widget
        solucion = QtGui.QGroupBox()
        solucion.setLayout(disenyo)

        return solucion


    def dibujar_intarfaz_mitad_superior(self):                          # Dibujo de la mitad superior de la interfaz
        # Botones
        self._boton_abrir = QtGui.QPushButton('Abrir')
        self._boton_abrir.clicked.connect(self.abrir)
        self._boton_abrir.setMaximumWidth(84)

        # Controles de edición
        self._text_ruta = QtGui.QLineEdit()
        self._text_ruta.setReadOnly(True)

        # Etiquetas
        label_archivo = QtGui.QLabel('Archivo:')
        # label_archivo.setMaximumWidth(45)

        # Diseño
        disenyo = QtGui.QHBoxLayout()
        disenyo.addWidget(label_archivo)
        disenyo.addWidget(self._text_ruta)
        disenyo.addWidget(self._boton_abrir)

        # Widget
        mitad_superior = QtGui.QGroupBox('Carga del archivo')
        mitad_superior.setLayout(disenyo)

        return mitad_superior


    def guardado(self):                                                 # Parte de la vista del procedimiento de guardado
            QtGui.QMessageBox.warning(self, 'Error de apertura', 'Error: Archivo <' + self._nombre_archivo + '> inaccesible')


    def guardar_como(self):                                             # Parte de la vista de la acción de guardar cómo
        return QtGui.QFileDialog.getSaveFileName(self, 'Guardar archivo')


    def imprimir(self):                                                 # Acción de imprimir
        impresion = QtGui.QPrintDialog()

        if impresion.exec_() == QtGui.QDialog.Accepted:
            # TODO: Establecer widget a imprimir self.textEdit.document().print_(impresion.printer())
            pass

        else:
            pass


