"""
1. Создать магазин в Базе данных
2. Поменять адресс xml файла
3. Поменять ID магазина в строке "51" и "53"
"""

import os, sys
import django
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()
import xml.etree.ElementTree as ET
from shop.models import Product, Price

tree = ET.parse('xml_imports/osnovnoi_products_pleer.xml')
root = tree.getroot()


succers_writes = 0
print(len(root.findall('.//offer')))
for prod in root.findall('.//offer'):

    product_data = {'name': None,
                    'price': None,
                    'url': None,
                    'sales_notes': None
                    }

    for data in product_data.keys():
        if data == 'name':
            if prod.find('model') != None:
                product_data['name'] = prod.find('name').text
            else:
                product_data['name'] = prod.find('name').text
        else:
            product_data[data] = prod.find(data).text

    get_product = None

    try:
        if prod.find('barcode').text != None:
            get_product = Product.objects.get(barcode=prod.find('barcode').text)
    except:
        try:
            if prod.find('model').text != None:
                get_product = Product.objects.get(vendorCode=prod.find('model').text)
        except:
            continue

    try:
        if get_product != None:
            product_data['shop_id'] = 3
            try:
                price_curent = get_product.prices.get(shop_id=3)
                price_curent.price = product_data['price']
                price_curent.name = product_data['name']
                price_curent.url = product_data['url']
                price_curent.save()
                get_product.save()
                succers_writes += 1
            except Price.DoesNotExist:
                get_price_shop = get_product.prices.create(**product_data)
                get_product.save()
                succers_writes += 1
    except Exception as error:
        print(error)

print(succers_writes)
print(len(root.findall('.//offer')))