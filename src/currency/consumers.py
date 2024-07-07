import json
from collections import OrderedDict
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer

from .utils import get_currency_api_request


class CurrencyConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = OrderedDict()
        self.message_key = datetime.now()

    async def connect(self):
        await self.channel_layer.group_add("default", self.channel_name)
        await self.accept()
        data = get_currency_api_request()
        await self.channel_layer.group_send(
            "default",
            {"type": "chat.message", "message": data},
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("default", self.channel_name)

    async def chat_message(self, event):
        message = event["message"]
        self.message_key = datetime.now()
        self.messages.update({f"{self.message_key}": message})
        self.messages.move_to_end(f"{self.message_key}", last=False)

        await self.send(text_data=json.dumps({"message": self.messages}))
