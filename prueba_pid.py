from simple_pid import PID
import random
import time
import matplotlib.pyplot as plt
import socket


# next create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)
port = 12345			
server_address = ('0.0.0.0', port)
sock.bind(server_address)
sock.setblocking(1)#Se pone el socket como bloqueante

print('starting up on {} port {}'.format(*server_address))
	
data, address = sock.recvfrom(1500)

asd = data[:-1].decode()
datos = asd.split(":")
velocidad_objetivo = datos[0]
inicio = int(datos[1])
print("Velocidad objetivo = " + str(velocidad_objetivo))

pid = PID(1, 0.1, 0.05, setpoint=int(velocidad_objetivo))
pid.output_limits = (-100, 100)
pid.sample_time = (0.1) # por defecto 0.01

lista = []
lista_tiempos = []

cont = 0
while True:
    cont += 1
    data, address = sock.recvfrom(1500)
    asd = data[:-1].decode()
    datos = asd.split(":")
    nuevo_dato = datos[0]
    print("Dato recibido:" + str(data.decode()))
    if("Hello" in data.decode()):
        print("Fin de la transmisión.")
        break
    dato = int(nuevo_dato)
    lista_tiempos.append(datos[1])
    control = pid(dato)/10 #Divido entre 20 para tener valores más comprensibles (de -5 a 5)
    lista.append(control)# Se guarda en una lista para las pruebas, en realidad tendría que ir modificando la velocidad del robot
    #time.sleep(0.25)
    if cont==100:
        break

print(lista)
#lista_tiempos.insert(0, inicio)
fig,ax = plt.subplots()
parsed = [(int(x)-inicio)/1000000 for x in lista_tiempos]
ax.plot(parsed, lista)
plt.show()


