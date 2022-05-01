import json
import time
import requests
import websocket
from threading import Thread
from typing import Any, Callable

WS_URL = "ws://localhost:8000/ws/robot/PiCar/"
API_URL = "http://localhost:8000/api/"

ws: 'ServerWebSocket' = None
websocket.enableTrace(False)


class ServerWebSocket(Thread):
    def __init__(self, on_message_callback) -> None:
        super().__init__()
        self.on_message_callback = on_message_callback
        self.connected = False
        self.ws = websocket.WebSocketApp(WS_URL,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def on_message(self, ws, message):
        data = json.loads(message)
        if data["type"] == "to.robot":
            self.on_message_callback(data["message"])
        else:
            print("Unknown message type: {}".format(data["type"]))

    def is_connected(self):
        return self.connected

    def on_error(self, ws, error):
        print("ServerWebSocket error: {}".format(error))

    def on_close(self, ws, close_status_code, close_msg):
        self.connected = False
        print("ServerWebSocket closed")

    def on_open(self, ws):
        self.connected = True
        print("ServerWebSocket connected")

    def run(self):
        self.ws.on_open = self.on_open
        self.ws.run_forever(ping_interval=10, ping_timeout=5)

    def close(self):
        self.ws.close()

    def send(self, data: object):
        self.ws.send(json.dumps(data))


def start_ws(on_message_callback: Callable[[object], Any]):
    global ws
    ws = ServerWebSocket(on_message_callback)
    ws.start()


def close_ws():
    ws.close()


def get_route_by_room(room: str):
    try:
        res = requests.get(API_URL + "routes/{}/".format(room))
        return res.json()
    except Exception:
        return None

def active(active: bool, route: object):
    data = {
        "active": active,
        "route": route
    }

    try:
        res = requests.put(API_URL + "robots/PiCar/active/", json=data)
        return res.json()
    except Exception:
        return None

def update_current_hall(hall: str):
    data = {
        "hall": hall
    }

    try:
        res = requests.put(API_URL + "robots/PiCar/hall/", json=data)
        return res.json()
    except Exception:
        return None


def obstacle_on_hall(hall: str):
    try:
        res = requests.put(API_URL + "statsHalls/{}/stopped/".format(hall))
        return res.json()
    except Exception:
        return None


def ui_next_direction():
    ws.send({"type": "to.ui", "message": {"type": "next_direction"}})

if __name__ == "__main__":
    def on_message(message):
        print("Received message: {}".format(message))

    route = get_route_by_room("01")
    start_ws(on_message)
    time.sleep(1)

    active(True, route)
    ui_next_direction()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        active(False, route)
        close_ws()
