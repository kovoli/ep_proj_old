import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()

import xml.etree.ElementTree as ET

from discounts.models import DiscountProduct, Category, Vendor

# For images
from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen

# For token Ozon
import requests, io, os

import re


def download_all_category_files():
    filename_list = []
    # 1. Бытовая техника, 2. Дом и сад
    categories_list = ['https://api.ozon.ru/PartnerTools/XmlFeed/11023170689840',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023172890760']

    url = 'https://api.ozon.ru/AuthServer/Token'
    data = {'grant_type': 'password', 'username': 'kovoli1985@gmail.com', 'password': 'Blagodat1985!'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url=url, data=data, headers=headers)  # Делаю запрос
    convert_tocken = r.json()  # Получаю json c токеном
    # получаю токен
    tokken = {'token': convert_tocken["access_token"]}

    for cat_url in categories_list:
        # Запрос категории с токеном
        request_cat_catalog = requests.get(cat_url, params=tokken)
        # Распаковка токена
        import zipfile
        zipfile = zipfile.ZipFile(io.BytesIO(request_cat_catalog.content))
        filename = zipfile.namelist()[0]
        zipfile.extractall('imports/')

        filename_list.append(filename)

    return filename_list

print(download_all_category_files())