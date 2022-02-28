import sys

lineas=[]

def parseo(ruta):
   file = open(ruta, "r")
   text=file.readlines()
   for line in text:
   	   lineas.append(line)

numHabitacion=sys.argv[1][:sys.argv[1].index(".")]
parseo(sys.argv[1])
for line in lineas:
    if "RR:" not in line:
        lineas.remove(line)        
    else:
        break


saltos=[]

for line in lineas[2:]:
     if "---" not in line:
        saltos.append(line[:line.index("\n")])
     else:
        break
try:
	saltos.pop()
except:
	pass

#remuevo caracteres \n

for salto in saltos:
    salto.replace("\n","")



saltosDefinitivos=[]

for i in range (len(saltos)):
    if i< (len(saltos)-1):
       if saltos[i] in saltos[i+1]:
          saltosDefinitivos.append(saltos[i])
          break
       else:
          saltosDefinitivos.append(saltos[i].replace("\t",""))

'''
saltosDefinitivos.pop(0)

'''
try:
	saltosDefinitivos.pop(len(saltosDefinitivos)-1)
except:
	pass
#print("SALTOS :")
#print(saltosDefinitivos)

'''
1 recto
2 derecha
3 abajo
4 izquierda
'''

movimientos=[]
for salto in saltosDefinitivos:
    aux=salto.split(".")
   # print(aux)
    if(str(aux[2]) == "1"):
        movimientos.append("recto")
    if(str(aux[2]) == "2"):
       movimientos.append("derecha")
    if(str(aux[2]) == "3"):
       movimientos.append("abajo")
    if(str(aux[2]) == "4"):
       movimientos.append("izquierda")

outputFile=open(numHabitacion+"ruta.txt","w")
for cruce in movimientos:
    outputFile.write(cruce)
    outputFile.write("\n")
numeroCruces=len(movimientos)

#for i in range(numeroCruces):
#   print("CRUCE "+str(i)+": "+str(movimientos[i]))
