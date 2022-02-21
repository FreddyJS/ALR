import os 

ruta = os.getcwd() + "/compartido/rutas/"
archivos = [f for f in os.listdir(ruta)]
txt = []

for i in archivos:
	if ".txt" in i:
		txt.append(i)

for i in txt:
	os.system("python3 " + "./compartido/scripts/parser.py " + ruta + "/" + i)

