HeurisPy
======

``HeurisPy`` es un framework orientado a objetos desarrollado en Python que busca 
auxiliar en la obtención de experiencia para el uso de heurísticas de búsqueda
local en problemas de optimización discreta.

Se ha diseñado con los siguientes principios en mente:

--``HeurisPy`` debe ser lo suficientemente general para permitir el planteamiento 
de varios problemas de optimización discreta.

--``HeurisPy`` debe ser accesible para usuarios con poca experiencia tanto en el
uso de heurísticas de búsqueda local como en programación.

--``HeurisPy`` debe contener varias heurísticas de búsqueda local listas para su
uso, así como una clase lo suficientemente general para permitir el agregado
de nuevas heurísticas.

--``HeurisPy`` debe permitir el trabajo en paralelo para facilitar el análisis
estadístico, y brindar herramientas que faciliten el trabajo.

Así, se espera que el usuario sólo deba preocuparse por la programación de su 
problema de optimización discreta y de experimentar con las heurísticas. ``HeurisPy``
se encargará de realizar las búsquedas y de brindar la información 
estadística para que el usuario pueda realizar una decisión informada.

``HeurisPy`` fue programado en Python 3.7 [(que se descarga aquí)](https://www.python.org/downloads/)
, y requiere de las siguientes bibliotecas para su funcionamiento:

--**numpy**: biblioteca para el cómputo científico en Python.

--**pathos**: biblioteca para el procesamiento en paralelo.

--**pandas**: biblioteca para el análisis de datos.

--**pyFPDF**: biblioteca para la generación de archivos PDF.

--**matplotlib**:biblioteca para la generación de gráficas.

--**tqdm**: biblioteca para la muestra del progreso de la exploración heurística.

Instalación
======


``HeurisPy`` está disponible como una biblioteca en PyPi, y se puede instalar con el
siguiente comando:

    pip install heurispy
    
Para comprobar su instalación, basta con...

Cómo funciona
======

``HeurisPy`` tiene tres clases principales que necesitan del usuario para funcionar:
Problema, Heurística, y Framework.

--**Problema**: Se encarga de retener la información del problema de 
optimización definido por el usuario.

--**Heurística**: Recibe los atributos del problema para iniciar la búsqueda de
soluciones con parámetros que el usuario determina.

--**Framework**: Dirige todos los procesos internos, como el procesamiento en
paralelo, la recolección de los datos y el llamado de métodos para la generación
de archivos.

Planteando el p.o.d.
======

Antes que nada, se necesita definir el problema de optimización discreta en ``HeurisPy``. Para esto, se debe:

--Definir un método para la creación de nuevas soluciones.

--Crear un método encargado de variar una solución existente.

--Crear una función objetivo a minimizar.

Por ejemplo, en el problema de coloración de grafos, se asignan colores a los vértices de un grafo, tratando de minimizar la cantidad 
de colores utilizados para colorearlo sin tener colores adyacentes repetidos. Como solución inicial, se le asigna a cada vértice un
color aleatorio (representado por un número entero). Esto se puede definir como sigue:

    def crear_solucion():
        import random
        nueva_solucion = []
        for indice in range(cantidad_vertices):
            nueva_solucion.append(random.randint(0, cantidad_vertices-1))
        return nueva_solucion

Para variar una solución dada, se elige un índice al azar de la solución, se verifican los vértices adyacentes y los valores de su 
coloración, y se elige un color diferente a todos ellos. Entonces:

    def variar_solucion(solucion):
        import random
        nueva_solucion = solucion.copy()
        longitud_solucion = len(nueva_solucion)
        indice_a_cambiar = random.randint(0, longitud_solucion-1)
        colores = list(range(cantidad_vertices))
        colores_adyacentes = obtener_colores_adyacentes(nueva_solucion, indice_a_cambiar)
        colores_disponibles = [color for color in colores if color not in colores_adyacentes]
        nueva_solucion[indice_a_cambiar] = random.choice(colores_disponibles)
        return nueva_solucion

La función objetivo comprueba la cantidad de colores diferentes en una solución, y qué tantos vértices adyacentes tienen colores repetidos. 
Esto es de la siguiente manera:

    def funcion_objetivo(solucion):
        costo_colores = costo_colores_diferentes(solucion)
        costo_adyacencia = costo_colores_adyacentes(solucion)
        return c_1 * costo_colores + c_2 * costo_adyacencia

Para finalizar, se necesita definir una instancia de la clase Problema, que se logra de la siguiente manera:

    from heurispy.problema import Problema
    
    problema_coloracion = Problema(dominio=crear_solucion , funcion_objetivo=funcion_objetivo, funcion_variacion_soluciones)
    
Los detalles de los métodos obtener_colores_adyacentes, costo_colores_diferentes, y costo_colores_adyacentes se encuentran en la 
ruta "/heurispy/ejemplos/problema_coloracion_grafo.py". Se necesitan definir para que la implementación de ejemplo funcione.
    
Preparando una heurística para su uso
======

Toda heurística implementada en ``HeurisPy`` es una clase que hereda de Heuristica. Para utilizar alguna en particular, 
sólo se necesita importar
la clase correspondiente, asignarle una instancia de la clase Problema, y definir algunos parámetros generales. Por ejemplo, para utilizar
la búsqueda tabú, se escribe lo siguiente:

    from heurispy.heuristicas.busqueda_tabu import BusquedaTabu
    
    busqueda_tabu = BusquedaTabu(problema_coloracion, max_iteraciones = 100000)
    
Sin embargo, todavía faltan definir parámetros específicos de la heurística que se desea utilizar.

Definiendo parámetros de la heurística
======

Para definir los parámetros específicos de la heurística, se necesita generar un diccionario. Un diccionario es un conjunto de valores a
los que se les asigna etiquetas llamadas "llaves". Para la búsqueda tabú:

    parametros_busqueda_tabu = dict(espacio_memoria=[50, 100, 150], max_busquedas_sin_mejoras=[100])
    
Este diccionario es la base que HeurisPy necesita para realizar la exploración. En este caso, se tienen tres tipos de corridas:

--Espacio en memoria = 50, Máximo de búsquedas sin mejora=100

--Espaio en memoria= 100, Máximo de búsquedas sin mejora=100

--Espacio en memoria= 150, Máximo de búsquedas sin mejora=100

Se necesita que todo valor en el diccionario sea una lista con todos los valores esperados en cada parámetro. El siguiente paso es determinar
cuántas repeticiones se realizarán para cada tipo de corrida.

Determinando repeticiones
======

Para determinar las repeticiones en cada tipo de corrida, se necesita del siguiente método:

    from heurispy.framework import genera_bloque_parametros
    
    lista_corridas = genera_bloque_parametros(parametros_busqueda_tabu, repeticiones=10)
    
Con esto, se realizarán 30 ejecuciones en total. 10 para el espacio en memoria de 50, 10 para el espacio en memoria de 100, y 10 para
el espacio en memoria de 150, todas con un máximo de búsqueda sin mejora de 100. 

Teniendo la heurística a utilizar definida por el problema y el total de ejecuciones a realizar, ya se puede iniciar el funcionamiento
de ``HeurisPy``.

Iniciando la explorción heurística
======

Basta utiliar los siguientes comandos para iniciar la exploración:

    from heurispy.framework import inicia_exploracion_heuristica
    
    inicia_exploracion_heuristica(busqueda_tabu, lista_corridas)
    
Como ``HeurisPy`` utiliza el procesamiento en paralelo, se puede definir la cantidad de nucleos a ocupar con el parámetro nucleos_cpu.
Por defecto, se utilizan todos los nucleos del procesdor.

Al iniciar el proceso, ``HeurisPy`` manda una barra de progreso (generada por la biblioteca tqdm) que contabiliza las ejecuciones a realizar, y
va arrojando información sobre la información recopilada y los archivos generados como resultados. 

Examinando los archivos
======

Al terminar la exploración heurística, se crean dos carpetas: Resultados, que guarda los resultados estadísticos y gráficos creados por
exploración heurística, e Información, que 
contiene los datos e información avanzada sobre las exploraciones realizadas. En Resultados, se genera una carpeta con el nombre de la
heurística utilizada, y dentro de ella se encuentran las exploraciones realizadas, cuyo nombre es la fecha y la hora en la que se finalizó
la exploración. Por ejemplo, si el ejemplo antes descrito terminó su exploración el 4 de julio del 2019 a las 12:31 pm, entonces se guardan
en la carpeta "2019-07-04---12-31". Aquí se encuentra un archivo pdf, cuyo nombre contiene la heurístca utilizada, los parámetros que 
corresponden a la corrida evaluada, y la fecha y hora en la que se generó el archivo. Se destaca que la información que despliegan los 
archivos es dependiente de la heurística, por lo que los datos estadísticos y gráficos pueden variar.

Como el desempeño de la heurística es muy dependiente de sus parámetros y del problema de optimización discreta, no hay una regla que 
determine la combinación ideal entre heurística y parámetros, por lo que es conveniente poner a prueba el p.o.d. con varias heurísticas y 
varias configuraciones de parámetros, buscando diversificar las corridas para obtener la mayor cantidad de información posible, y buscar 
consistencia en los resultados.

    
