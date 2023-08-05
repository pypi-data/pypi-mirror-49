Esta librería permite leer y modificar fichero de configuración en tiempo de ejecución.   
Los parámetros en los ficheros de configuración se dividirán en sectores al estilo de la librería *configparser*.

Uso de la clase y ejemplos:    
[https://github.com/gmolino/parsini](https://github.com/gmolino/parsini)

## Versiones

##### 0.0.1

* Parsea fichero de configuración, crear nuevos parámetros y/o actualiza los existentes.
* Sobrescribe el fichero de configuración o crear copia con los nuevos parámetros o actualizados.

##### 0.0.2

* from parsini import Parsini (fixed)

##### 0.0.3

* No crea nuevo parámetro si existente.
* Comprueba el nombre del valor antes de actulizar para modificar repeticiones.

##### 0.0.4

* Recarga parámetros por defecto en la llamada al método *read(True)* para evitar incongruencia en caso de múltiples instancias.
