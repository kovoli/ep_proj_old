"""
1. Создать магазин в Базе данных
2. Поменять адресс xml файла
3. Поменять ID магазина в строке "51" и "53"
"""

import os, sys, requests
import django
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()
import xml.etree.ElementTree as ET
from shop.models import Product, Price
from fuzzywuzzy import fuzz

url = 'http://export.admitad.com/ru/webmaster/websites/1009966/products/export_adv_products/?feed_id=5308&code=8daef5a69b&user=kovoli&template=40740'

r = requests.get(url)

with open('imports/ogo_price.xml', 'wb') as xml_file:
    xml_file.write(r.content)

tree = ET.parse('imports/ogo_price.xml')
root = tree.getroot()

update_product = 0
create_product = 0
errors = 0
for prod in root.findall('.//offer'):

    product_data = {'name': None,
                    'price': None,
                    'oldprice': None,
                    'url': None,
                    'sales_notes': None,
                    'categoryId': None,
                    }

    for data in product_data.keys():
        if prod.find(data) != None:
            product_data[data] = prod.find(data).text
        else:
            continue

    get_product = None

    try:
        if prod.find('barcode') != None:
            get_product = Product.objects.get(barcode=prod.find('barcode').text)
        elif prod.find('vendorCode') != None:
            get_product = Product.objects.get(vendorCode=prod.find('vendorCode').text)
        else:
            continue
    except:
        continue

    prod_category = get_product.category.name
    cat_xml = root.find(".//category/[@id='{}']".format(product_data['categoryId'])).text
    result_contain = fuzz.partial_ratio(prod_category, cat_xml)

    try:
        if get_product != None:
            product_data['shop_id'] = 9
            del product_data['categoryId']
            try:
                if result_contain > 50:
                    price_curent = get_product.prices.get(shop_id=9)
                    price_curent.price = product_data['price']
                    price_curent.name = product_data['name']
                    price_curent.url = product_data['url']
                    price_curent.save()
                    get_product.save()
                    update_product += 1
            except Price.DoesNotExist:
                if result_contain > 50:
                    get_price_shop = get_product.prices.create(**product_data)
                    get_product.save()
                    create_product += 1
    except Exception as error:
        errors += 1

print('Цен созданно', create_product)
print('Цен обновленно', update_product)
print('Ошибок', errors)
print(len(root.findall('.//offer')))