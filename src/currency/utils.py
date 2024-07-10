import json
from random import randint

import requests
from django.conf import settings


def get_currency_api_request(url: str) -> dict:
    """функция получения данных о курсе пары доллар-рубль."""

    if settings.DEBUG:
        data = json.dumps({"data": {"USDRUB": randint(1, 1000)}})
    else:
        try:
            data = requests.get(url).text
        except Exception as e:
            data = json.dumps({"data": str(e)})

    return json.loads(data).get("data", {})
