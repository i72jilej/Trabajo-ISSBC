## Descripción
Trabajo práctico de la asignatura Ingeniería de Sistemas Software Basados en Conocimiento (en adelante ISSBC), de la Universidad de Córdoba (UCO)

El campo a cubrir es la planificación. La tarea a realizar es de planificación, la cual consistirá en, dada la información de una hipotética frábica: sus máquinas y sus conexiones entre las mismas, se encargará de obtener la manera más óptima de utilizarlas.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b646ed416c2449b59f1fa0047c3fd8a8)](https://www.codacy.com/app/veltys/Trabajo-ISSBC?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Veltys/Trabajo-ISSBC&amp;utm_campaign=Badge_Grade)

## Realizado por
- Rafael Carlos Méndez Rodríguez (i82meror@uco.es / veltys@veltys.es)
- Julio Domingo Jiménez Ledesma (i72jilej@uco.es / ralkaishagtten@gmail.com)


## Sistemas
- **main.py**: Lanzador de la aplicación. Se encarga de la configuración inicial y el lanzamiento.
- **modelo.py**: Modelo de la aplicación. Se encarga de todas las funciones relacionadas con el procesamiento y obtención de datos a través de RDFLib
- **vista.py**: Vista de la aplicación. Se encarga de toda la parte gráfica: ventana principal, cuadros de diálogo, ventanas modales, ventanas de aviso, etc.
- **controlador.py**: Controlador de la aplicación. Se encarga de llevar a cabo la conexión del resto de sistemas. 
- **maquinas\*.nt**: Ejemplos de archivos de datos en formato NTriples que la aplicación necesita para llevar a cabo su función.


## Historial de versiones
- 1.0.0 -> 30/05/2018:
    - Implementación inicial de los sistemas y, en consecuencia, de la aplicación.
- 1.0.1 -> 15/06/2018:
    - Mejoras en el tratamiento de las cadenas en Python 2.
- 1.1.0 -> 15/06/2018:
    - Implementado finalmente el procedimiento para generar múltiples soluciones.
- 1.1.1 -> 17/06/2018:
    - Mejora de la calidad del código.
    - Arreglo de compatibilidad con Python 2.


## Agradecimientos, fuentes consultadas y otros créditos
* A la [documentación oficial de Python 3](https://docs.python.org/3/), por motivos evidentes.
* A la [documentación oficial de Python 2](https://docs.python.org/2/), por los mismos motivos.
* A la [documentación del depurador remoto de PyDev](http://www.pydev.org/manual_adv_remote_debugger.html), porque para llevar a cabo las correcciónes de compatibilidad, es más simple ejecutar en remoto y depurarlo.
* A la [documentación oficial de RDFLib](https://rdflib.readthedocs.io/en/stable/), porque ha facilitado enormemente su aplicación.
* A *Matthew Lincoln*, por su ["Using SPARQL to access Linked Open Data"](https://programminghistorian.org/es/lecciones/sparql-datos-abiertos-enlazados), porque ha sido muy útil para optimizar las consultas SPARQL.
* A *Oscar Campos*, por [la entrada sobre hilos en la web *www.genbetadev.com*](https://www.genbetadev.com/python/multiprocesamiento-en-python-threads-a-fondo-introduccion), la cual ha permitido llevar a cabo el procesamiento paralelo.


## Por hacer (*TODO*)
- [x] Optimizar la compatibilidad con Python 2.
- [x] Añadir el procedimiento para generar múltiples soluciones.
- [ ] Rehacer el comportamiento de los controles gráficos de control para que se puedan introducir datos también por texto.
- [ ] Portar la interfaz gráfica a PyQt5.
