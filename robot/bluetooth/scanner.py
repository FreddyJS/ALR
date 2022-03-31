import os
import time
import socket

import subprocess
from signal import SIGKILL
from threading import Thread


UDP_PORT = 12345
SERVER_ADDRESS = "0.0.0.0"

bluetoothScanner: 'BluetoothScanner' = None
socketScanner: 'SocketScanner' = None


class BluetoothScanner():
    def __init__(self, deviceName: str):
        folder = os.path.dirname(__file__)
        self.src_path = os.path.join(folder, "scanner.c")
        self.exe_path = os.path.join(folder, "scanner")

        self.deviceName = deviceName
        self.started = False
        self.process = None
        self.compile()

    def start(self):
        print("Starting BluetoothScanner process...")
        self.process = subprocess.Popen(
            [self.exe_path, "-h", self.deviceName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.started = True
        print("BluetoothScanner process started")

    def is_alive(self):
        return False if not self.started else self.process.poll() is None

    def kill(self):
        print("Killing BluetoothScanner process...")
        self.started = False
        self.process.kill()
        print("BluetoothScanner process killed")

    def compile(self):
        print("Compiling BluetoothScanner...")
        ret = subprocess.call(
            ["gcc", "-o", self.exe_path, self.src_path, "-lbluetooth"])
        if ret != 0:
            raise Exception("Compile BluetoothScanner failed")
        print("BluetoothScanner compiled")


class SocketScanner(Thread):
    def __init__(self, deviceName, processSample):
        super().__init__()
        self.processSample = processSample
        self.deviceName = deviceName
        self._running = False

    def kill(self):
        self._running = False
        self.join()

    def run(self):
        print("Starting socket scanner")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((SERVER_ADDRESS, UDP_PORT))
        self.socket.setblocking(0)

        self._running = True
        while self._running:
            try:
                data, addr = self.socket.recvfrom(1024)
                print("Received: " + data.decode("utf-8") + " from " + str(addr))

                self.processSample(data.decode("utf-8")[0:-1])
            except Exception:
                time.sleep(0.1)

        self.socket.close()
        print("SocketScanner terminated")


def start(deviceName, onReceive):
    global socketScanner, bluetoothScanner
    socketScanner = SocketScanner(deviceName, onReceive)
    bluetoothScanner = BluetoothScanner(deviceName)
    socketScanner.start()
    bluetoothScanner.start()

    time.sleep(0.1)
    if not bluetoothScanner.is_alive():
        err: bytes = bluetoothScanner.process.stderr.readline()
        print("BluetoothScanner failed: " + err.decode("utf-8")[0:-1])
        socketScanner.kill()
        socketScanner.join()
        exit(1)
    else:
        print("Scanner started")


def stop():
    global socketScanner, bluetoothScanner
    socketScanner.kill()
    bluetoothScanner.kill()
