import os 

ruta = os.getcwd() + "/compartido/"
archivos = [f for f in os.listdir(ruta)]
txt = []

for i in archivos:
	if ".txt" in i:
		txt.append(i)

for i in txt:
	os.system("python3 " + ruta + "/parser.py " + ruta + "/" + i)

