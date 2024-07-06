from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from config.celery import app

from .utils import get_currency_api_request


@app.task
def get_currency_task():
    message = get_currency_api_request()
    channel_layer = get_channel_layer("default")
    async_to_sync(channel_layer.group_send)(
        "default",
        {"type": "chat.message", "message": message},
    )
