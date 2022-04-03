import json
import requests
import websocket
from threading import Thread

WS_URL = "ws://localhost:8000/ws/robot/PiCar/"
API_URL = "http://localhost:8000/api/"

ws: 'ServerWebSocket' = None
websocket.enableTrace(False)


class ServerWebSocket(Thread):
    def __init__(self, on_message_callback) -> None:
        super().__init__()
        self.on_message_callback = on_message_callback
        self.ws = websocket.WebSocketApp(WS_URL,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def on_message(self, ws, message):
        data = json.loads(message)
        if data["type"] == "to.robot":
            print(data)
            self.on_message_callback(data)

    def on_error(self, ws, error):
        print("ServerWebSocket error: {}".format(error))

    def on_close(self, ws, close_status_code, close_msg):
        print("ServerWebSocket closed")

    def on_open(self, ws):
        print("ServerWebSocket connected")

    def run(self):
        self.ws.on_open = self.on_open
        self.ws.run_forever(ping_interval=10, ping_timeout=5)

    def close(self):
        self.ws.close()

    def send(self, data: object):
        self.ws.send(json.dumps(data))


def start_ws(on_message_callback):
    global ws
    ws = ServerWebSocket(on_message_callback)
    ws.start()


def close_ws():
    ws.close()


def get_route_by_room(room):
    res = requests.get(API_URL + "routes/{}".format(room))
    return res.json()
