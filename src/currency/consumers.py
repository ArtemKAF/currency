from collections import OrderedDict
from datetime import datetime
from json import dumps, loads

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from redis import from_url

from .utils import get_currency_api_request


class CurrencyConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = OrderedDict()
        self.message_key = datetime.now()
        self.history_vault = from_url(settings.REDIS_URI)

    async def connect(self):
        await self.channel_layer.group_add("default", self.channel_name)
        await self.accept()
        if self.history_vault.exists("default_history"):
            self.messages.update(loads(self.history_vault.get("default_history")))
        data = get_currency_api_request()
        await self.channel_layer.group_send(
            "default",
            {"type": "chat.message", "message": data},
        )

    async def disconnect(self, close_code):
        if len(self.messages) == 10:
            self.messages.popitem()
        self.history_vault.setex("default_history", 600, dumps(self.messages))
        await self.channel_layer.group_discard("default", self.channel_name)

    async def chat_message(self, event):
        message = event["message"]

        if len(self.messages) == 10:
            self.messages.popitem()

        self.message_key = datetime.now()
        self.messages.update({f"{self.message_key}": message})
        self.messages.move_to_end(f"{self.message_key}", last=False)

        await self.send(text_data=dumps({"message": self.messages}))
