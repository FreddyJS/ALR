import json

from channels.generic.websocket import AsyncWebsocketConsumer

class UIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join a group
        await self.channel_layer.group_add(
            "test_group",
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            "test_group",
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to group
        await self.channel_layer.group_send(
            "test_group",
            {
                'type': 'chat_message',
                'message': message + " - from backend"
            }
        )

        # Echo message back to client
        await self.send(text_data=json.dumps({
            'message': message + " - from backend"
        }))
    
    # Receive message from group
    async def chat_message(self, event):
        message = event['message']
        print("A message was received: " + message)