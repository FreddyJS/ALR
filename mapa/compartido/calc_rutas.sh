#!/bin/bash
h23=10.23.0.23
h30=10.34.0.30
h61=10.6.0.61

ping -c 1 -R $h23 > /media/sf_compartido/h23.txt
ping -c 1 -R $h30 > /media/sf_compartido/h30.txt
ping -c 1 -R $h61 > /media/sf_compartido/h61.txt
