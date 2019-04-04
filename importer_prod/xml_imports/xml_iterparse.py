import os, sys
import django
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()
import xml.etree.ElementTree as ET


from shop.models import Product, Category, Vendor, Price

# For images
from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen

import re

category_list = {}
con = 0
none_url = 0
link_count = 0
for event, elem in ET.iterparse('10500.xml', events=('start', )):

    #if elem.tag == 'category':

        #category_list[elem.attrib['id']] = elem.text
    # Находит тэг offer
    if elem.tag == 'offer':
        print(event)


        # Создаем словарь для Product
        product_data = {}

        # Создаем словарь для Price ###!!! Поменять shop.id для соответствующего магазина !!!###
        price_data = {'name': None, 'price': None, 'oldprice': None,
                      'url': None, 'sales_notes': None, 'shop_id': 1}

        # Пробегаем по всем тэгам в offer
        for data in elem:
            if data.tag == 'url':
                print(event)
                print(data, data.text)
                link_text = data.text
                if link_text != None:
                    price_data['url'] = 'https://f.gdeslon.ru/cf/0c7e8158ad?mid=12027&goto=' + data.text[:link_text.index('?')]
                    link_count += 1
                else:
                    none_url += 1
            elif data.tag == 'price':
                price_data['price'] = data.text
            elif data.tag == 'name':
                product_data['name'] = data.text
                price_data['name'] = data.text
                print(data.text)
        con += 1
    elem.clear()

print(con)
print(none_url)
print(link_count)