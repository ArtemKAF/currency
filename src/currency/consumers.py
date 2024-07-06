import json

from channels.generic.websocket import AsyncWebsocketConsumer


class CurrencyConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = {}
        self.counter = 0

    async def connect(self):
        await self.channel_layer.group_add("default", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("default", self.channel_name)

    async def chat_message(self, event):
        message = event["message"]
        self.messages.update({f"{self.counter}": message})
        self.counter += 1

        await self.send(text_data=json.dumps({"message": self.messages}))
