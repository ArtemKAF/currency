# currency
Реализация получения и отображения информации о курсе валютной пары доллар-рубль
при помощи запросов к API ресурса https://currate.ru/.
Отображение результатов запросов происходит собщениями через websocket.

## Стек технологий:

[![Python 3.12.1][Python-badge]][Python-url]
[![Django][Django-badge]][Django-url]
[![Channels][Channels-badge]][Channels-url]
[![Celery][Celery-badge]][Celery-url]
[![requests][requests-badge]][requests-url]
[![Redis][Redis-badge]][Redis-url]
[![Nginx][Nginx-badge]][Nginx-url]

## Как запустить проект локально (необходим установленный Python3.12.1, poetry и redis):

Клонировать репозиторий:

```
git clone git@github.com:ArtemKAF/currency.git
```
Перейти в директорию, в которую были скачаны исходные файлы проекта при клонировании:

```
cd currency/
```

Cоздать виртуальное окружение и установить необходимые зависимости командой:

```
poetry install --no-root
```

Активировать созданное виртуальное окружение командой:

```
poetry shell
```

В корневой директории проекта создать файл .env и заполнить его переменными
окружения по шаблону из .env.example

Примечание для значений DEBUG:


- True - сервер разработки будет обрабатывать подключение main.js.
- False - необходимо дополнительно настраивать сервер для обработки статики.


Перейти в директорию src и выполнить следующие команды:

```shell
python manage.py migrate
python manage.py runserver
```
После успешного запуска сервера разработки эндпоинт для получения информации о
курсе валюты будет доступен про адресу http://localhost:8000/get-current-usd/

Примечание:

Для запуска процесса обновления информации по расписанию необходимо параллельно
запустить celery worker и celery beat scheduller.

Для этого в дополнительных окнах терминала из директории src проекта с активированным виртуальным окружением необходимо выполнить команды:
- во втором окне терминала для celery worker-a
```shell
celery -A config.celery worker --loglevel info
```
- в третьем окне терминала для celery beat sheduller-а
```shell
celery -A config beat --loglevel info
```
В случае успеха, через каждые 30 секунд информация о курсе валюты будет обновлена.


### Запуск проекта в docker контенерах:

В корневой директории проекта подготовлены файлы:
- docker-compose.yaml (для запуска проекта вцелом вместе с redis)
- docker-compose-redis.yaml (для запуска только redis)

Команда для запуска:
```shell
docker compose -f <соответствующий файл> up -d
```


<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/

[Python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white

[Django-url]: https://github.com/django/django

[Django-badge]: https://img.shields.io/badge/Django-0c4b33?style=for-the-badge&logo=django&logoColor=white

[channels-url]: https://channels.readthedocs.io/en/latest/

[channels-badge]: https://img.shields.io/badge/channels-grey?style=for-the-badge&logo=django-channels&logoColor=white

[Celery-url]: https://docs.celeryq.dev/en/stable/index.html

[Celery-badge]: https://img.shields.io/badge/Celery-a9cc54?style=for-the-badge&logo=celery&logoColor=white

[requests-url]: https://requests.readthedocs.io/en/latest/index.html

[requests-badge]: https://img.shields.io/badge/requests-grey?style=for-the-badge&logo=requests&logoColor=white

[Redis-url]: https://redis.readthedocs.io/en/stable/index.html

[Redis-badge]: https://img.shields.io/badge/Redis-red?style=for-the-badge&logo=redis&logoColor=white

[Nginx-url]: https://nginx.org

[Nginx-badge]: https://img.shields.io/badge/nginx-009900?style=for-the-badge&logo=nginx&logoColor=white
