import os, sys
import django
sys.path.append('..')
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

"""
def download_all_category_files():
    filename_list = []
    # 1. Бытовая техника
    # 2. Дом и сад
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

print(download_all_category_files())"""

tree = ET.parse('imports/10500.xml')
root = tree.getroot()

categories = root.findall('.//category')
posts = root.findall('.//offer')
print(len(posts))
cat_db = Category.objects.values('id', 'name')


def check_field_not_none(field):
    if field is not None:
        return field
    else:
        return None


def description_beautify(text):
    regex = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\:)\s"
    subst = "</br>"
    return re.sub(regex, subst, text, 0, re.MULTILINE)


def parameter_beatify(param):
    charact = []
    for par in param:
        if 'unit' in par.attrib:
            charact.append('<tr><td>' + par.attrib['name'] + ':' + '</td><td>' + par.text + ' ' + par.attrib['unit'] + '</td></tr>')
        else:
            charact.append('<tr><td>' + par.attrib['name'] + ':' + '</td><td>' + par.text + '</td></tr>')
    return ''.join(charact)


def def_category(category_id):
    id_cat_name = root.find(".//category[@id='{}']".format(category_id))  # Нахожу катеорию через id в загруженном xml
    id_cat_name = id_cat_name.text
    for i in Category.objects.values('id', 'name'):  # Извлекаю из базы данных все категории и ищу соответствующую категорию
        if i['name'] == id_cat_name:
            return i['id']


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


def create_discount_prod():
    product_data = {'name': None, 'prod_id': off.attrib['id'], 'description': None,
                    'param': None, 'categoryId': None,
                    'price': None, 'oldprice': None,
                    'url': None,
                    }
    try:
        for data in product_data.keys():
            if off.find(data) is None:
                continue
            if data == 'url':
                product_data[data] = 'https://f.gdeslon.ru/cf/0c7e8158ad?mid=12027&goto=' + off.find(data).text[
                                                                                            :off.find(data).text.index(
                                                                                                '?')]
            elif data == 'description':
                product_data[data] = description_beautify(off.find(data).text)
            elif data == 'param':
                product_data[data] = parameter_beatify(off.findall(data))
            elif data == 'categoryId':
                del product_data['categoryId']
                product_data['category_id'] = def_category(off.find(data).text)
            else:
                product_data[data] = off.find(data).text

        vendor = vendor_get_or_create(off.find('vendor').text)
        product = DiscountProduct.objects.create(**product_data)
        product.vendor = vendor
        # Image
        original_picture = check_field_not_none(off.find('picture').text)
        input_file = BytesIO(urlopen(original_picture, ).read())
        product.discount_image.save(product_data['name'] + '.jpg', ContentFile(input_file.getvalue()), save=False)
        # Save Image
        product.save()
    except Exception as error_create:
        print(error_create)

def update_discount_data(get_discount):
    product_data = {'price': None, 'oldprice': None,}
    try:
        for data in product_data.keys():
            if off.find(data) is None:
                continue
            else:
                product_data[data] = off.find(data).text
        get_discount.price = product_data['price']
        get_discount.price = product_data['oldprice']
        get_discount.save()
    except Exception as error_update:
        print(error_update)


list_of_discounts = DiscountProduct.objects.all().values_list('prod_id', flat=True)

del_discount = 0
create_discount = 0
update_discount = 0
for off in root.findall('.//offer'):

    # Скидки НЕТ
    if off.find('oldprice') == None:
        # Товар удаляется из DB
        if off.attrib['id'] in list_of_discounts:
            del_discount += 1
            try:
                DiscountProduct.objects.get(prod_id=off.attrib['id']).delete()
            except Exception as error:
                print(error)
        else:
            continue
    # Скидка ЕСТЬ
    elif off.find('oldprice') != None:
        # Скидки нет в DB
        if off.attrib['id'] not in list_of_discounts:
            create_discount += 1
            # Создаётся скидка
            create_discount_prod()
        # Скидка есть в DB
        elif off.attrib['id'] in list_of_discounts:
            update_discount += 1
            get_discount = DiscountProduct.objects.get(prod_id=off.attrib['id'])
            update_discount_data(get_discount)


print(len(root.findall('.//offer')))
print('Скидок удалилось :', del_discount)
print('Скидок создалось :', create_discount)
print('Скидка обновилась:', update_discount)