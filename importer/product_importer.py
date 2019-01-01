import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()

import xml.etree.ElementTree as ET


from shop.models import Product, Category, Vendor, Price

# For images
from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen

import re


tree = ET.parse('10500.xml')
root = tree.getroot()

categories = root.findall('.//category')


cat_db = Category.objects.values('id', 'name')


def check_field_not_none(field):
    if field is not None:
        return field
    else:
        return None



# Helper Functions
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


def add_price_to_product(off, product):
    offer_price_data = {'price': 0, 'oldprice': None, 'name': None, 'url': None, 'sales_notes': None,
                        'shop_id': 1, 'product_id': product.id}
    for data in offer_price_data.keys():
        print(off.find(data))
        if off.find(data) is None:
            continue
        else:
            offer_price_data[data] = off.find(data).text

    return Price.objects.create(**offer_price_data)
# TODO Проверку на наличие поста
# TODO Впараметрах бывают видеообзоры; при наличие добавить в поле video




succers_writes = 0
errors = []
for off in root.findall('.//offer'):

    product_data = {'name': None, 'description': None,
                    'param': None, 'vendorCode': None,
                    'barcode': None, 'categoryId': None,
                    }
    try:
        for data in product_data.keys():
            if off.find(data) is None:
                continue
            if data == 'description':
                product_data[data] = description_beautify(off.find(data).text)
            elif data == 'param':
                product_data[data] = parameter_beatify(off.findall(data))
            elif data == 'categoryId':
                del product_data['categoryId']
                product_data['category_id'] = def_category(off.find(data).text)
            else:
                product_data[data] = off.find(data).text

        vendor = vendor_get_or_create(off.find('vendor').text)

        #original_picture = check_field_not_none(off.find('picture').text)
        #input_file = BytesIO(urlopen(original_picture, ).read())

        product = Product.objects.create(**product_data)
        product.vendor = vendor
        add_price_to_product(off, product)
        #product.product_image.save(name + '.jpg', ContentFile(input_file.getvalue()), save=False)
        product.save()
        print('Succes')
        succers_writes += 1
    except Exception as error:
        errors.append(error)
        print(error)

print(succers_writes)
print(len(root.findall('.//offer')))
print(errors)
