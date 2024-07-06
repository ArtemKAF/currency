from django.urls import re_path

from .consumers import CurrencyConsumer

websocket_urlpatterns = [
    re_path("ws/currency/", CurrencyConsumer.as_asgi()),
]
