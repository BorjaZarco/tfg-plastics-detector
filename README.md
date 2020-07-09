# Detector de Microplásticos

Este repositorio contiene el código necesario para realizar las detecciones de 4 tipos de microplásticos a partir de imágenes digitales de los mismos. 

Esta aplicación depende de una implementación en [Keras de Yolov3](https://github.com/qqwweee/keras-yolo3) hecha por [@qqwweee](https://github.com/qqwweee). Quiero aprovechar para agradecerle la implementación de esta librería ya que facilitó la elaboración de este prototipo. 


## Instalación

Se recomienda tener instalado en el dispositivo [Python 3.6](https://www.python.org/downloads/release/python-360/) o [Python 3.7](https://www.python.org/downloads/release/python-370/), así como [PIP](https://pypi.org/project/pip/) como gestor de paquetes de este lenguaje. El propio repositorio contiene un pequeño fichero ejecutable, `script.sh`, que se encarga de la correcta instalación del proyecto y sus dependencias. De todas formas, a continuación se detallan los pasos necesarios para cumplir con todos los pasos.  

En primer lugar, la instalación de esta aplicación se requiere la descarga de la implementación en [Keras de Yolov3](https://github.com/qqwweee/keras-yolo3) en la carpeta raíz del proyecto. Además, es necesario renombrar la misma de `keras-yolo3` a `keras_yolo3` para el correcto funcionamiento de la aplicación.

A continuación, se ha de pasar a la descarga de todas las librerías de python de las que depende este proyecto. Existe un pequeño fichero de texto, `requirements.txt`, que lista todas estas dependencias, con la versión específica cada una de ellas que se utilizó durante el desarrollo. Con el comando `pip install -r requirements.txt`, se procedería a la instalación de todas estas bibliotecas de forma automática.

Por último, se ha de descargar (y descomprimir si fuera necesario), la carpeta `model_weights` que está alojada en la nube a través de este [enlace](https://drive.google.com/drive/folders/1nPKPucKVG8r_TReNu0ubfdo356mnXunf?usp=sharing). Hay que asegurarse que esta carpeta se encuentre en la raíz del proyecto.

## Uso

El uso de esta aplicación es bastante simple, únicamente hay que respetar ciertas consideraciones. En este proyecto hay dos directorios fundamentales: `in` y `out`. 

- `in`: aquí se han de localizar todas las imágenes que se deseen pasar por el detector antes de iniciar dicho proceso.

- `out`: una vez finalizado el proceso de detección, en este directorio se van a alojar los resultados. Estos resultados se agruparán en carpetas que tendrán en mismo nombre que la imagen original a la que corresponde. Dentro de las mismas se encontrarán, a su vez, dos subdirectorios que contienen, respectivamente, una imagen con las detecciones remarcadas y un csv con todos los detalles relativos al resultado.

Para la realización de una detección se ha situar en la carpeta raíz del proyecto y ejecutar el siguiente comando:

```
python detector.py
```

