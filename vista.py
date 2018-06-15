#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Title         : vista.py
# Description   : Vista del programa
# Author        : Julio Domingo Jiménez Ledesma
# Author        : Rafael Carlos Méndez Rodríguez
# Date          : 15-06-2018
# Version       : 1.0.1
# Usage         : import vista o from vista import ...
# Notes         : 


from __future__ import unicode_literals


import sys                                                                  # Funcionalidades varias del sistema

from PyQt4 import QtCore, QtGui                                             # Módulo de interfaz de usuario de PyQt4


class respuestas():
    DESCARTAR               = 0
    CANCELAR                = 1
    GUARDAR                 = 2

    diccionario             = []
    diccionario.append(QtGui.QMessageBox.Discard)
    diccionario.append(QtGui.QMessageBox.Cancel)
    diccionario.append(QtGui.QMessageBox.Save)


class ventana_vista(QtGui.QMainWindow):                                     # Parte de la vista de la ventana
    _TITULO_APP = 'Planificador de cadena de montaje'

    _aviso_valores = QtGui.QMessageBox.No

    _num_hijos = 1000                                                       # Número de hilos a utilizar (soluciones posibles)

    _prob_heuristica = 50


    def __init__(self):                                                     # Parte de la vista del constructor de la clase; al ser una ventana, inicializa la misma
        if sys.version_info[0] >= 3:                                        # Llamada al método equivalente de la clase padre
            super().__init__()

        else:
            super(ventana_vista, self).__init__()

        self.crearAcciones()                                                # Crer los menús, barras de herramientas y acciones que éstos dispararán
        #                                                                   # Es importante crear las acciones lo primero, ya que el resto de elementos dependen de ellas
        self.crearMenus()

        self.crearBarraDeHerramientas()

        self.dibujar_interfaz()                                             # Dibujar la interfaz

        self._widget_principal = QtGui.QWidget(self)                        # Establecer el widget principal

        self._widget_principal.setLayout(self._disenyo)                     # Establecer el diseño del widget

        self.setCentralWidget(self._widget_principal)                       # Establecer el widget central

        self.setWindowIcon(QtGui.QIcon('./iconos/000-checklist.png'))       # Establecer el icono de la ventana principal

        self.setWindowTitle(self._TITULO_APP)                               # Se establece el título de la ventana

        self.statusBar().showMessage('Esperando archivo')                   # Se establece el mensaje para barra de estado

        self.setMinimumSize(0, 720)                                         # Parámetros de tamaño

        self.resize(1280, 720)


    def acercaDe(self):                                                     # Ventana modal que muestra la información de "Acerca de"
        QtGui.QMessageBox.about(self, 'Acerca de', '''<p>Trabajo de planificación creada por Julio Domingo Jiménez Ledesma (i72jilej) y Rafael Carlos Méndez Rodríguez (i82meror)</p>
<p>Icono usado en "Nuevo" por <a href="https://www.flaticon.com/authors/yannick">Yannick</a><br />
Icono usado en "Abrir" por <a href="https://www.flaticon.com/authors/simpleicon">SimpleIcon</a><br />
Iconos usados en la ventana principal, "Guardar", "Calcular", "Acerca de" y "Acerca de Qt" por <a href="https://www.flaticon.com/authors/freepik">Freepic</a><br />
Iconos usados en "Guardar como" y "Salir" por <a href="https://www.flaticon.com/authors/smashicons">Smashicons</a><br />
Icono usado en "Imprimir" por <a href="https://www.flaticon.com/authors/dave-gandy">Dave Gandy</a><br />
Todos ellos autores de <a href="https://www.flaticon.com/">www.flaticon.com</a></p>
''')


    def acercaDeQt(self):                                                   # Ventana modal que muestra la información de "Acerca de Qt"
        QtGui.qApp.aboutQt()


    def actualizar_valor_heuristica(self):                                  # Actualiza el valor de la variable y el campo de texto al desplazar el deslizante
        if (self._slider_heuristica.value() > 75 or self._slider_heuristica.value() < 25) and self._aviso_valores == QtGui.QMessageBox.No:
            self._aviso_valores = self.confirmar_valores()

            if self._aviso_valores == QtGui.QMessageBox.No:
                self._slider_heuristica.setValue(50)

        self._prob_heuristica = self._slider_heuristica.value()

        self._slider_heuristica.setToolTip(str(self._slider_heuristica.value()))

        self._text_heuristica.setText(str(self._slider_heuristica.value()) + ' %')


    def actualizar_valor_hijos(self):                                       # Actualiza el valor de la variable y el campo de texto al desplazar el deslizante
        if self._slider_hijos.value() > 5000 and self._aviso_valores == QtGui.QMessageBox.No:
            self._aviso_valores = self.confirmar_valores()

            if self._aviso_valores == QtGui.QMessageBox.No:
                self._slider_hijos.setValue(1000)

        self._num_hijos = self._slider_hijos.value()

        self._slider_hijos.setToolTip(str(self._slider_hijos.value()))

        self._text_hijos.setText(str(self._slider_hijos.value()))


    def apertura(self, modo, *args):                                        # Parte de la vista del procedimiento de apertura
        if modo == 'abrir':
            return str(QtGui.QFileDialog.getOpenFileName(self, 'Abrir archivo', filter = 'Base de conocimiento NTriples (*.nt);;Todos los archivos (*.*)'))

        elif modo == 'error':
            return QtGui.QMessageBox.warning(self, 'Aviso', 'El formato del archivo es incorrecto o no ha podido ser cargado')

        elif modo == 'dominio':
            self._text_dominio.setText(args[0])
            self._text_ruta.setText(args[1])

            self.setWindowTitle(self._TITULO_APP + ' ➡ ' + args[1])

            return True


    def aviso_carga(self, accion):
        return QtGui.QMessageBox.information(self, 'Imposible ' + accion, 'Información: No es posible ' + accion + ' ya que aún no se han realizado cálculos')


    def calcular(self, modo, *args):                                        # Parte de la vista de la realización de los cálculos necesarios
        if modo == 'error':
            QtGui.QMessageBox.warning(self, 'Imposible calcular', 'Aviso: No es posible calcular ya que aún no se ha cargado ningún archivo')
        
        elif modo == 'desarrollo':
            self._text_desarrollo.setText(self._text_desarrollo.toPlainText() + args[0] + "\n")
        elif modo == 'solucion':

            self._text_solucion.setText(self._text_solucion.toPlainText() + args[0] + "\n")


    def confirmar_modificado(self, accion):                                 # Confirmación de las modificaciones antes de realizar una operación que pueda destruirlas
        if self.modificado():
            mensaje = QtGui.QMessageBox()
            mensaje.setIcon(QtGui.QMessageBox.Question)
            mensaje.setWindowTitle('Aviso')
            mensaje.setText('Hay cálculos no guardados. ¿Desea guardarlos antes de ' + accion + '?')
            mensaje.setStandardButtons(QtGui.QMessageBox.Discard | QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel)
            mensaje.setDefaultButton(QtGui.QMessageBox.Cancel)

            boton_descartar = mensaje.button(QtGui.QMessageBox.Discard)
            boton_descartar.setText('Descartar')

            boton_guardar = mensaje.button(QtGui.QMessageBox.Save)
            boton_guardar.setText('Guardar')

            boton_cancelar = mensaje.button(QtGui.QMessageBox.Cancel)
            boton_cancelar.setText('Cancelar')

            return mensaje.exec_()

        else:
            return QtGui.QMessageBox.Discard


    def confirmar_valores(self):                                            # Confirmación de valores extermos
        mensaje = QtGui.QMessageBox()
        mensaje.setIcon(QtGui.QMessageBox.Question)
        mensaje.setWindowTitle('Aviso')
        mensaje.setText('Valores extremos podrían dar resultados pobres o inesperados. ¿Está seguro?')
        mensaje.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        mensaje.setDefaultButton(QtGui.QMessageBox.No)

        return mensaje.exec_()


    def crearAcciones(self):                                	       	    # Creación de las acciones asociadas al menú y a la barra de herramientas
        self.nuevoAcc           = QtGui.QAction('&Nuevo',           self, shortcut = QtGui.QKeySequence.New,    statusTip = 'Crea un nuevo archivo',                                triggered = self.nuevo          )
        self.abrirAcc           = QtGui.QAction('&Abrir...',        self, shortcut = QtGui.QKeySequence.Open,   statusTip = 'Abre un archivo existente',                            triggered = self.abrir          )
        self.guardarAcc         = QtGui.QAction('&Guardar',         self, shortcut = QtGui.QKeySequence.Save,   statusTip = 'Guarda el archivo',                                    triggered = self.guardar        )
        self.guardarComoAcc     = QtGui.QAction('Guardar c&omo',    self, shortcut = QtGui.QKeySequence.SaveAs, statusTip = 'Guarda el archivo con un nombre distinto',             triggered = self.guardar_como   )
        self.imprimirAcc        = QtGui.QAction('Im&primir',        self, shortcut = QtGui.QKeySequence.Print,  statusTip = 'Imprime el archivo',                                   triggered = self.imprimir       )
        self.salirAcc           = QtGui.QAction('&Salir',           self, shortcut = 'Alt+F4',                  statusTip = 'Sale de la aplicación',                                triggered = self.close          )
        self.calcularAcc        = QtGui.QAction('&Calcular',        self, shortcut = 'F4',                      statusTip = 'Comienza los cálculos',                                triggered = self.calcular       )
        self.acercaDeAcc        = QtGui.QAction('&Acerca de',       self, shortcut = 'F1',                      statusTip = 'Muestra la ventana "Acerca de"',                       triggered = self.acercaDe       )
        self.acercaDeQtAcc      = QtGui.QAction('Acerca de &Qt',    self,                                       statusTip = 'Muestra la ventana "Acerca de" de la librería Qt',     triggered = self.acercaDeQt     )

        self.nuevoAcc.          setIcon(QtGui.QIcon('./iconos/001-add-new-document.png')                            )
        self.abrirAcc.          setIcon(QtGui.QIcon('./iconos/002-folder-black-open-shape.png')                     )
        self.guardarAcc.        setIcon(QtGui.QIcon('./iconos/003-save-icon.png')                                   )
        self.guardarComoAcc.    setIcon(QtGui.QIcon('./iconos/004-technology.png')                                  )
        self.imprimirAcc.       setIcon(QtGui.QIcon('./iconos/005-printing-tool.png')                               )
        self.salirAcc.          setIcon(QtGui.QIcon('./iconos/006-logout.png')                                      )
        self.calcularAcc.       setIcon(QtGui.QIcon('./iconos/007-calculator.png')                                  )
        self.acercaDeAcc.       setIcon(QtGui.QIcon('./iconos/008-about-us.png')                                    )
        self.acercaDeQtAcc.     setIcon(QtGui.QIcon('./iconos/009-presenter-talking-about-people-on-a-screen.png')  )


    def crearBarraDeHerramientas(self):                     	            # Creación de la barra de herramientas
        self._toolbar = self.addToolBar('Barra de herramientas')
        self._toolbar.addAction(self.nuevoAcc)
        self._toolbar.addAction(self.abrirAcc)
        self._toolbar.addAction(self.guardarAcc)
        self._toolbar.addAction(self.guardarComoAcc)
        self._toolbar.addSeparator()
        self._toolbar.addAction(self.calcularAcc)
        self._toolbar.addSeparator()
        self._toolbar.addAction(self.salirAcc)

        self._toolbar.setMovable(False)                                     # Hace la barra inamovible


    def crearMenus(self):                                   	            # Creación de los menús
        self._menu_archivo = self.menuBar().addMenu('&Archivo')
        self._menu_archivo.addAction(self.nuevoAcc)
        self._menu_archivo.addAction(self.abrirAcc)
        self._menu_archivo.addAction(self.guardarAcc)
        self._menu_archivo.addAction(self.guardarComoAcc)
        self._menu_archivo.addSeparator()
        self._menu_archivo.addAction(self.imprimirAcc)
        self._menu_archivo.addSeparator()
        self._menu_archivo.addAction(self.salirAcc)

        self._menu_accion = self.menuBar().addMenu('A&cción')
        self._menu_accion.addAction(self.calcularAcc)

        self._menu_ayuda = self.menuBar().addMenu("A&yuda")
        self._menu_ayuda.addAction(self.acercaDeAcc)
        self._menu_ayuda.addAction(self.acercaDeQtAcc)


    def dibujar_interfaz(self):                                             # Dibujo de la interfaz
        self._disenyo = QtGui.QVBoxLayout()                                 # Establecimiento del tipo de interfaz
        self._disenyo.addWidget(self.dibujar_intarfaz_tercio_superior())    # Añadiendo widgets a base de funciones externas
        self._disenyo.addWidget(self.dibujar_intarfaz_tercio_central())
        self._disenyo.addWidget(self.dibujar_intarfaz_tercio_inferior())


    def dibujar_intarfaz_tercio_central(self):                              # Dibujo del tercio central de la interfaz
        # Diseño
        disenyo = QtGui.QHBoxLayout()
        disenyo.setMargin(0)
        disenyo.setSpacing(0)

        # Widgets
        disenyo.addWidget(self.dibujar_interfaz_tercio_central_mitad_izquierda())
        disenyo.addWidget(self.dibujar_interfaz_tercio_central_mitad_derecha())

        # Widget
        mi_widget = QtGui.QGroupBox('Control')
        mi_widget.setLayout(disenyo)
        mi_widget.setStyleSheet('QGroupBox QGroupBox { border: 0px; }')

        return mi_widget


    def dibujar_interfaz_tercio_central_mitad_derecha(self):                # Dibujo de la parte de heurística del tercio central de la interfaz
        # Controles de edición
        self._slider_heuristica = QtGui.QSlider(QtCore.Qt.Horizontal)
        self._slider_heuristica.setMinimum(0)
        self._slider_heuristica.setMaximum(100)
        self._slider_heuristica.setValue(50)
        self._slider_heuristica.setTickPosition(QtGui.QSlider.TicksBelow)
        self._slider_heuristica.setTickInterval(1)

        # Eventos de los controles
        self._slider_heuristica.setToolTip(str(self._slider_heuristica.value()))
        self._slider_heuristica.valueChanged.connect(self.actualizar_valor_heuristica)

        # Diseño
        disenyo = QtGui.QVBoxLayout()

        # Widgets
        disenyo.addWidget(self.dibujar_interfaz_tercio_central_mitad_derecha_mitad_superior())
        disenyo.addWidget(self._slider_heuristica)

        # Widget
        mi_widget = QtGui.QGroupBox()
        mi_widget.setLayout(disenyo)

        return mi_widget


    def dibujar_interfaz_tercio_central_mitad_derecha_mitad_superior(self): # Dibujo de la mitad superior del tercio central de la interfaz
        # Etiquetas
        label_heuristica = QtGui.QLabel('Probabilidad heurística:')
        label_heuristica.setMaximumWidth(150)

        # Controles de edición
        self._text_heuristica = QtGui.QLineEdit()
        self._text_heuristica.setMaximumWidth(40)
        self._text_heuristica.setReadOnly(True)                             # TODO: Rehacerlo de modo que, editándolo, valide y cargue valores
        self._text_heuristica.setText(str(self._prob_heuristica) + ' %')

        # Diseño
        disenyo = QtGui.QHBoxLayout()

        # Widgets
        disenyo.addWidget(label_heuristica)
        disenyo.addWidget(self._text_heuristica)
        disenyo.setAlignment(QtCore.Qt.AlignLeft)

        # Widget
        mi_widget = QtGui.QGroupBox()
        mi_widget.setLayout(disenyo)

        return mi_widget


    def dibujar_interfaz_tercio_central_mitad_izquierda(self):              # Dibujo de la parte de heurística del tercio central de la interfaz
        # Controles de edición
        self._slider_hijos = QtGui.QSlider(QtCore.Qt.Horizontal)
        self._slider_hijos.setMinimum(100)
        self._slider_hijos.setMaximum(10000)
        self._slider_hijos.setValue(1000)
        self._slider_hijos.setTickPosition(QtGui.QSlider.TicksBelow)
        self._slider_hijos.setTickInterval(100)

        # Eventos de los controles
        self._slider_hijos.setToolTip(str(self._slider_hijos.value()))
        self._slider_hijos.valueChanged.connect(self.actualizar_valor_hijos)

        # Diseño
        disenyo = QtGui.QVBoxLayout()

        # Widgets
        disenyo.addWidget(self.dibujar_interfaz_tercio_central_mitad_izquierda_mitad_superior())
        disenyo.addWidget(self._slider_hijos)

        # Widget
        mi_widget = QtGui.QGroupBox()
        mi_widget.setLayout(disenyo)

        return mi_widget


    def dibujar_interfaz_tercio_central_mitad_izquierda_mitad_superior(self): # Dibujo de la mitad superior del tercio central de la interfaz
        # Etiquetas
        label_hijos = QtGui.QLabel('Cantidad de hilos buscadores de soluciones simultáneos:')
        label_hijos.setMaximumWidth(350)

        # Controles de edición
        self._text_hijos = QtGui.QLineEdit()
        self._text_hijos.setMaximumWidth(40)
        self._text_hijos.setReadOnly(True)                                  # TODO: Rehacerlo de modo que, editándolo, valide y cargue valores
        self._text_hijos.setText(str(self._num_hijos))

        # Diseño
        disenyo = QtGui.QHBoxLayout()

        # Widgets
        disenyo.addWidget(label_hijos)
        disenyo.addWidget(self._text_hijos)
        disenyo.setAlignment(QtCore.Qt.AlignLeft)

        # Widget
        mi_widget = QtGui.QGroupBox()
        mi_widget.setLayout(disenyo)

        return mi_widget


    def dibujar_intarfaz_tercio_inferior(self):                             # Dibujo del tercio inferior de la interfaz
        # Diseño
        disenyo = QtGui.QHBoxLayout()
        disenyo.setMargin(0)
        disenyo.setSpacing(0)

        # Widgets
        disenyo.addWidget(self.dibujar_interfaz_tercio_inferior_mitad_izquierda_dominio())
        disenyo.addWidget(self.dibujar_interfaz_tercio_inferior_mitad_derecha())

        # Widget
        mi_widget = QtGui.QGroupBox('Resultados')
        mi_widget.setLayout(disenyo)
        mi_widget.setStyleSheet('QGroupBox QGroupBox { border: 0px; }')

        return mi_widget


    def dibujar_interfaz_tercio_inferior_mitad_derecha(self):               # Dibujo de la mitad derecha del tercio inferior de la interfaz
        # Diseño
        disenyo = QtGui.QVBoxLayout()
        disenyo.setMargin(0)
        disenyo.setSpacing(0)

        # Widgets
        disenyo.addWidget(self.dibujar_interfaz_tercio_inferior_mitad_derecha_desarrollo())
        disenyo.addWidget(self.dibujar_interfaz_tercio_inferior_mitad_derecha_solucion())

        # Widget
        mi_widget = QtGui.QGroupBox()
        mi_widget.setLayout(disenyo)
        mi_widget.setStyleSheet('QGroupBox QGroupBox { border: 0px; }')

        return mi_widget


    def dibujar_interfaz_tercio_inferior_mitad_derecha_desarrollo(self):    # Dibujo de la parte de desarrollo de la mitad derecha del tercio inferior de la interfaz
        # Etiquetas
        label_desarrollo = QtGui.QLabel('Desarrollo:')

        # Controles de edición
        self._text_desarrollo = QtGui.QTextEdit()
        self._text_desarrollo.setReadOnly(True)

        # Diseño
        disenyo = QtGui.QVBoxLayout()

        # Widgets
        disenyo.addWidget(label_desarrollo)
        disenyo.addWidget(self._text_desarrollo)

        # Widget
        mi_widget = QtGui.QGroupBox()
        mi_widget.setLayout(disenyo)
        mi_widget.setMinimumWidth(650)

        return mi_widget


    def dibujar_interfaz_tercio_inferior_mitad_derecha_solucion(self):      # Dibujo de la parte de solución de la mitad derecha del tercio inferior de la interfaz
        # Etiquetas
        label_solucion = QtGui.QLabel('Solución:')

        # Controles de edición
        self._text_solucion = QtGui.QTextEdit()
        self._text_solucion.setReadOnly(True)

        # Diseño
        disenyo = QtGui.QVBoxLayout()

        # Widgets
        disenyo.addWidget(label_solucion)
        disenyo.addWidget(self._text_solucion)

        # Widget
        mi_widget = QtGui.QGroupBox()
        mi_widget.setLayout(disenyo)

        return mi_widget


    def dibujar_interfaz_tercio_inferior_mitad_izquierda_dominio(self):     # Dibujo de la parte de dominio de la mitad izquierda del tercio inferior de la interfaz
        # Etiquetas
        label_dominio = QtGui.QLabel('Dominio:')

        # Controles de edición
        self._text_dominio = QtGui.QTextEdit()
        self._text_dominio.setReadOnly(True)

        # Diseño
        disenyo = QtGui.QVBoxLayout()

        # Widgets
        disenyo.addWidget(label_dominio)
        disenyo.addWidget(self._text_dominio)

        # Widget
        mi_widget = QtGui.QGroupBox()
        mi_widget.setLayout(disenyo)
        mi_widget.setMaximumWidth(400)
        mi_widget.setMinimumWidth(400)

        return mi_widget


    def dibujar_intarfaz_tercio_superior(self):                             # Dibujo del tercio superior de la interfaz
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

        # Widgets
        disenyo.addWidget(label_archivo)
        disenyo.addWidget(self._text_ruta)
        disenyo.addWidget(self._boton_abrir)

        # Widget
        mi_widget = QtGui.QGroupBox('Carga del archivo')
        mi_widget.setLayout(disenyo)

        return mi_widget


    def guardado(self):                                                     # Parte de la vista del procedimiento de guardado
            QtGui.QMessageBox.warning(self, 'Error de apertura', 'Error: Archivo <' + self._nombre_archivo + '> inaccesible')


    def guardar_como(self, modo):                                           # Parte de la vista de la acción de guardar cómo
        if modo == 'nombre':
            return str(QtGui.QFileDialog.getSaveFileName(self, 'Guardar archivo', filter = 'Documentos de texto (*.txt);;Todos los archivos (*.*)'))

        elif modo == 'error':
            return self.aviso_carga('guardar')


    def imprimir(self, modo):                                               # Acción de imprimir
        if modo == 'imprimir':
            impresion = QtGui.QPrintDialog()

            if impresion.exec_() == QtGui.QDialog.Accepted:
                self._text_solucion.document().print_(impresion.printer())

            else:
                pass

        elif modo == 'error':
            return self.aviso_carga('imprimir')


    def __del__(self):                                                      # Parte de la vista del destructor de la clase
        # if sys.version_info[0] >= 3:                                      # Llamada al método equivalente de la clase padre
            # super().__del__()                                             # Comentado porque la clase padre (QtGui.QMainWindow) no parece tener un método destructor
        # else:
            # super(ventana_vista, self).__del__()

        pass


