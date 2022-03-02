#!/bin/bash

./ruta.py $1 $2 $3 $4
cat rutas/$2_$3.txt
rm -rf rutas
