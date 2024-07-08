from collections import OrderedDict
from datetime import datetime
from json import dumps, loads
from typing import Any, Mapping, OrderedDict

import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from .utils import get_currency_api_request


class CurrencyConsumer(AsyncWebsocketConsumer):
    """Класс-обработчик событий websocket-соединения."""

    def __init__(self, *args, **kwargs) -> None:
        """Метод инициализации класса."""

        super().__init__(*args, **kwargs)

        self.messages: OrderedDict = OrderedDict()
        self.message_key: datetime = datetime.now()
        self.history_vault: redis.Redis = redis.from_url(settings.REDIS_URI)

    async def connect(self) -> None:
        """Метод подключения к websocket-соединению."""

        await self.channel_layer.group_add("default", self.channel_name)
        await self.accept()

        if self.history_vault.exists("default_history") and (
            (history := self.history_vault.get("default_history")) is not None
        ):
            self.messages.update(loads(history))

        data = get_currency_api_request()
        await self.channel_layer.group_send(
            "default",
            {"type": "chat.message", "message": data},
        )

    async def disconnect(self, close_code: Any) -> None:
        """Метод отключения от websocket-соединения."""

        if len(self.messages) == 10:
            self.messages.popitem()
        self.history_vault.setex("default_history", 600, dumps(self.messages))

        await self.channel_layer.group_discard("default", self.channel_name)

    async def chat_message(self, event: Mapping[str, Any]) -> None:
        """Метод обработки событий websocket-соединения с типом "chat.message"."""

        message = event["message"]

        if len(self.messages) == 10:
            self.messages.popitem()

        self.message_key = datetime.now()
        self.messages.update({f"{self.message_key}": message})
        self.messages.move_to_end(f"{self.message_key}", last=False)

        await self.send(text_data=dumps({"message": self.messages}))
