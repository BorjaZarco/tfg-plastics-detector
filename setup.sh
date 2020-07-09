#!/bin/bash

echo "Iniciando instalación..."

echo "Clonando dependencias de github"
git clone https://github.com/qqwweee/keras-yolo3.git
mv keras-yolo3 ./keras_yolo3

echo "Instalando librerías con pip..."
pip3 install -r requirements.txt


echo "Instalación finalizada! Diríjase a https://drive.google.com/drive/folders/1nPKPucKVG8r_TReNu0ubfdo356mnXunf?usp=sharing para descargarse los pesos"