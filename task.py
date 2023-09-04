import os
import re

import requests
import telebot

from bs4 import BeautifulSoup
from celery import Celery

import django
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avito_notifier.settings")
django.setup()

from bot.models import TelegramUser
from offers.models import Offer


# set the default Django settings module for the 'celery' program.
app = Celery("avito_notifier", broker='redis://localhost:6379')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

old = []

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'task.parse_avito',
        'schedule': 30.0,
    },
}
app.conf.timezone = 'UTC'

black_list = [
    'rx', '5600', 'radeon', '5700', '5600xt', '5700xt', '1660', '1660super', 'gtx',
    'под заказ', 'rx 5600 xt', 'gtx 1660 super', 'pulse',
]

white_list = [
    'rtx 2060', 'rtx2060', 'super',
]


def download_image(url):
    response = requests.get(url=url)
    if response.ok:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()

        return File(img_temp, os.path.basename(url) + '.webp')


@app.task
def parse_avito():
    URL_TEMPLATE = 'https://www.avito.ru/volgograd/tovary_dlya_kompyutera/klaviatury_i_myshi-ASgBAgICAUTGB7xO?cd=1&q=logitech+g+pro+superlight&s=104'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    r = requests.get(URL_TEMPLATE, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    items = soup.select('div[data-marker="item"]')

    bot = telebot.TeleBot("6551507249:AAH5XhUMyWa5e8fDn-Ke6cKq7NrOA44cl-o")

    for item in items:
        title = item.select_one('a[itemProp="url"]')['title']
        description = item.select_one('meta[itemProp="description"]')['content']
        price = int(item.select_one('meta[itemProp="price"]')['content'])
        href = 'https://avito.ru' + item.select_one('a[itemProp="url"]')['href']

        if not re.search('|'.join(black_list), title, re.I) and 5000 <= price <= 7000:
            image = item.select_one('ul[class="photo-slider-list-OqwtT"] > li')['data-marker'].replace(
                'slider-image/image-',
                '')
            image = download_image(image)

            offer, created = Offer.objects.get_or_create(
                title=title,
                description=description,
                price=price,
                link=href,
                defaults={'photo': image},
            )
            if created:
                for user in TelegramUser.objects.filter(subscribed=True):
                    bot.send_message(user.chat_id, href)
