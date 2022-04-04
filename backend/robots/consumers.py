import json
import string

from .models import Robot
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class RobotConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.robot: Robot = None

    @database_sync_to_async
    def get_robot(self, robot_id) -> Robot or None:
        try:
            return Robot.objects.get(robot_id=robot_id)
        except Robot.DoesNotExist:
            return None

    @database_sync_to_async
    def create_robot(self, robot_id: str, robot_channel: str, ui_channel: str = None) -> Robot:
        robot = Robot(robot_id=robot_id, robot_channel=robot_channel, ui_channel=ui_channel)
        robot.save()
        return robot

    @database_sync_to_async
    def update_robot(self, robot: Robot, data: dict) -> Robot:
        for key, value in data.items():
            setattr(robot, key, value)
        robot.save()
        return robot

    async def connect(self):
        print(self.channel_layer)
        self.robot_id: string = self.scope['url_route']['kwargs']['robot_id']
        self.connection_type: string = self.scope['url_route']['kwargs']['connection_type']
        print("A connection was made: robot_name: {}, connection_type: {}".format(self.robot_id, self.connection_type))

        self.robot: Robot = await self.get_robot(self.robot_id)

        if (self.connection_type == "robot"):
            if (self.robot is None):
                # Create a new robot
                self.robot: Robot = await self.create_robot(self.robot_id, self.channel_name)
            else:
                # Update the robot
                self.robot: Robot = await self.update_robot(self.robot, {'robot_channel': self.channel_name})

            await self.channel_layer.group_add(self.robot.robot_id, self.channel_name)
            await self.accept()
        elif (self.connection_type == "ui"):
            # Receiving UI connection
            if (self.robot is None):
                # Robot not found, UI must wait for the robot to connect
                await self.close()
            else:
                # Robot found, UI can stablish the connection
                self.robot = await self.update_robot(self.robot, {'ui_channel': self.channel_name})
                
                await self.channel_layer.group_add(self.robot.robot_id, self.channel_name)
                await self.accept()

                await self.send(text_data=json.dumps({
                    'message': "UI connected"
                }))
                
        else:
            await self.close()

    async def disconnect(self, close_code):
        # TODO: Should we delete the db entry if the UI or the robot is disconnected?
        await self.channel_layer.group_discard(self.robot.robot_id, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type: string = data['type']
        print("Message Received: " + str(data['message']) + " (type: " + message_type + ")")

        if (message_type == "to.robot"):
            # Received message from UI, forward it to the robot
            await self.channel_layer.group_send(self.robot.robot_id, data)
        elif (message_type == "to.ui"):
            # Received message from robot, forward it to the UI
            await self.channel_layer.group_send(self.robot.robot_id, data)

    async def to_ui(self, data: dict):
        if (self.connection_type == "robot"):
            return

        await self.send(text_data=json.dumps(data))

    async def to_robot(self, data: dict):
        if (self.connection_type == "ui"):
            return

        await self.send(text_data=json.dumps(data))