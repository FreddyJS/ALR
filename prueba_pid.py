from simple_pid import PID
import random
import time
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

velocidad_objetivo = data[:-1].decode()
print("Velocidad objetivo = " + str(velocidad_objetivo))

pid = PID(1, 0.1, 0.05, setpoint=int(velocidad_objetivo))
pid.output_limits = (-100, 100)
pid.sample_time = (0.1) # por defecto 0.01
lista = []

while True:

    data, address = sock.recvfrom(1500)
    data = data [:-1]
    print("Dato recibido:" + str(data.decode()))
    if("Hello" in data.decode()):
        print("Fin de la transmisión.")
        break
    dato = int(data.decode())
    
    control = pid(dato)/20 #Divido entre 20 para tener valores más comprensibles (de -5 a 5)
    lista.append(control)# Se guarda en una lista para las pruebas, en realidad tendría que ir modificando la velocidad del robot
    #time.sleep(0.25)

print(lista)

