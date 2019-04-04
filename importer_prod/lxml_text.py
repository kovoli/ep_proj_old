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

import re, unidecode

from lxml import etree




count = 0
link_count = 0
succers_writes = 0
errors = 0
category_list = {}

# Loop over all categories and make a dictionary
for event, category in etree.iterparse('imports/15500.xml', tag="categories"):
    for child in category:
        category_list[child.attrib['id']] = child.text


def vendor_get_or_create(vendor):
    change_vendor_name = {'Bosch GmbH': 'Bosch', 'Bosch GmbH,Bosch': 'Bosch'}
    if vendor in change_vendor_name:
        vendor = change_vendor_name[vendor]
    elif vendor == None:
        return None
    try:
        return Vendor.objects.get(name=vendor.lower())
    except Vendor.DoesNotExist:
        obj = Vendor(name=vendor.lower())
        return obj.save()

def description_beautify(text):
    if text == None:
        return 'С подробным описанием товара и ценами можно ознакомиться на сайте продавца.'
    else:
        regex = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\:)\s"
        subst = "</br>"
        return re.sub(regex, subst, text, 0, re.MULTILINE)

def video_rewiew_param(param):
    youtube_url = 'https://www.youtube.com/embed/'
    if 'Видеообзор' in param:
        a = param['Видеообзор']
        return youtube_url + a[a.index('=') + 1:]
    else:
        return None

# Loop over all offers
for event, element in etree.iterparse('imports/15500.xml', tag="offer"):
    count += 1

    picture = ''
    vendor = ''
    param_data = {}

    # Создаем словарь для Product
    product_data = {'name': None, 'description': None,
                    'param': None, 'vendorCode': None,
                    'barcode': None, 'category_id': None}



    # Создаем словарь для Price ###!!! Поменять shop.id для соответствующего магазина !!!###
    price_data = {'name': None, 'price': None, 'oldprice': None,
                  'url': None, 'sales_notes': None, 'shop_id': 1}
    for child in element:
        # URL (price_data) Для других магазинов ###!!! убрать ссылку от "GdeSlon"!!!###
        if child.tag == 'url':
            price_data['url'] = 'https://f.gdeslon.ru/cf/0c7e8158ad?mid=12027&goto=' + child.text[:child.text.index('?')]
            link_count += 1
        # PRICE (price_data)
        elif child.tag == 'price':
            price_data['price'] = child.text
        elif child.tag == 'oldprice':
            price_data['oldprice'] = child.text
        # CATEGORY
        elif child.tag == 'categoryId':
            get_category_id = Category.objects.get(name=category_list[child.text])
            product_data['category_id'] = int(get_category_id.id)
        # IMAGE Обрабатывается дальше
        elif child.tag == 'picture':
            picture = child.text
        # SALES_NOTE (price_data)
        elif child.tag == 'sales_notes':
            price_data['sales_notes'] = child.text
        # NAME (price_data) and (product_data)
        elif child.tag == 'name':
            product_data['name'] = child.text
            price_data['name'] = child.text
        # VENDOR (product_data)
        elif child.tag == 'vendor':
            vendor = child.text
        # VENDORCODE (product_data)
        elif child.tag == 'vendorCode':
            product_data['vendorCode'] = child.text
        # DESCRIPTION
        elif child.tag == 'description':
            product_data['description'] = description_beautify(child.text)
        elif  child.tag == 'barcode':
            product_data['barcode'] = child.text
        elif child.tag == 'param':
            if 'unit' in child.attrib:
                param_data[child.attrib['name']] = [child.text, child.attrib['unit']]
                product_data['param'] = param_data
            else:
                param_data[child.attrib['name']] = [child.text]
                product_data['param'] = param_data


    try:
        vendor = vendor_get_or_create(vendor)
        video = video_rewiew_param(param_data)
        input_file = BytesIO(urlopen(picture, ).read())
        product = Product.objects.create(**product_data)
        product.vendor = vendor
        product.video = video
        price_data['product_id'] = product.id
        Price.objects.create(**price_data).save()
        product.product_image.save(product_data['name'] + '.jpg', ContentFile(input_file.getvalue()), save=False)
        product.save()
        succers_writes += 1

    except Exception as error:
        errors += 1
        print(error)
    element.clear()
print(count)
print(succers_writes)
print(category_list)