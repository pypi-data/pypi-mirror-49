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

HeurisPy está disponible como una biblioteca en PyPi, y se puede instalar con el siguiente comando:

    pip install heurispy
    
Y se debería instalar en su versión más reciente.
    
Se puede probar el funcionamiento de HeurisPy con cualquiera de los scripts contenidos en
la carpeta "ejemplos", que se tiene incluída al momento e instalar el framework.
