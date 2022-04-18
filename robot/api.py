import json
import time
import requests
import websocket
from threading import Thread
from typing import Any, Callable

WS_URL = "ws://192.168.1.131:8000/ws/robot/R02/"
API_URL = "http://192.168.1.131:8000/api/"

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
    res = requests.get(API_URL + "routes/{}".format(room))
    return res.json()


def update_current_hall(hall: str):
    assert(ws.is_connected(), "WebSocket Disconnected cannot send messages")
    data = {
        "type": "to.ui",
        "message": {
            "hall": hall
        }
    }

    ws.send(data)


if __name__ == "__main__":
    def on_message(message):
        print("Received message: {}".format(message))

    start_ws(on_message)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        close_ws()
