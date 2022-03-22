from simple_pid import PID
import random
import time
import socket



'''

randomlist = []
for i in range(0,10):
    n = random.randint(1,100)
    randomlist.append(n)


randomlist.clear()
#randomlist = [23, 96, 40, 53, 85, 86, 76, 85, 55, 96]
randomlist = [23, 35, 50, 55, 40, 75, 80, 20, 50, 50, 50]
print(randomlist)


for element in randomlist:
    control = pid(element)
    print (control)
    time.sleep(0.25)	

'''

# next create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)


# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345			

server_address = ('0.0.0.0', port)
sock.bind(server_address)
sock.setblocking(1)
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
    
    control = pid(dato)
    lista.append(control)
    #time.sleep(0.25)

print(lista)

