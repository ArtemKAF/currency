from typing import Any, Optional

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from config.celery import app

from .utils import get_currency_api_request


@app.task
def get_currency_task() -> None:
    """
    Метод получения у стороннего API данных о курсе пары доллар-рубль и
    отправки их в канал определенный в настройках как "default".
    """

    message: dict = get_currency_api_request()
    channel_layer: Optional[Any] = get_channel_layer("default")
    if channel_layer is not None:
        async_to_sync(channel_layer.group_send)(
            "default",
            {"type": "chat.message", "message": message},
        )
