import socket
import threading


UDP_PORT = 12345
SERVER_ADDRESS = "0.0.0.0"

listener: threading.Thread = None
sock: socket.socket = None
running: bool = False

def start_comms(onReceive):
    # Starts a thread to listen for udp packages
    global running
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_ADDRESS, UDP_PORT))

    print("Listening for UDP packets on port " + str(UDP_PORT))
    while running:
        data, addr = sock.recvfrom(1024)
        onReceive(data.decode('utf-8')[0:-1])
        print("Received: " + data.decode("utf-8") + " from " + str(addr))
    
    sock.close()
    print("Stopped listening for UDP packets")

def start(onReceive):
    global running, listener
    listener = threading.Thread(target=start_comms, args=[onReceive])
    running = True
    listener.start()

def stop():
    global running, listener
    running = False
    listener.join()