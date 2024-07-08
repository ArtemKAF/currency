from json import dumps, loads
from random import randint

from django.conf import settings
from requests import get


def get_currency_api_request() -> dict:
    """функция получения данных о курсе пары доллар-рубль."""

    key = settings.API_KEY
    url = settings.CURRENCY_API_URL

    data = get(f"{url}?get=rates&pairs=USDRUB&key={key}").text

    return loads(data).get("data", {})
