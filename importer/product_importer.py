import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()

import xml.etree.ElementTree as ET


from shop.models import Product, Category

# For images
from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen

import re


tree = ET.parse('1133722.xml')
root = tree.getroot()

categories = root.findall('.//category')


cat_db = Category.objects.values('id', 'name')


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
    print(id_cat_name.text)
    id_cat_name = id_cat_name.text
    for i in Category.objects.values('id', 'name'):  # Извлекаю из базы данных все категории и ищу соответствующую категорию
        if i['name'] == id_cat_name:
            return i['id']

# TODO Зделать добавление и проверку Вендора
# TODO Проверку на наличие поста
# TODO Проверку на наличее содержания поля



print(len(root.find('.//offers')))

for offer in root.findall('.//offer')[10:]:
    try:
        name = offer.find('name').text
        description = description_beautify(offer.find('description').text)
        characteristic = parameter_beatify(offer.findall('param'))
        barcode = offer.find('barcode').text
        vendorCode = offer.find('vendorCode').text
        category_id = def_category(offer.find('categoryId').text)
        vendor = offer.find('vendor').text
        original_picture = offer.find('picture').text
        input_file = BytesIO(urlopen(original_picture, ).read())

        product = Product.objects.create(name=name, description=description, characteristic=characteristic,
                                         barcode=barcode, vendorCode=vendorCode, category_id=category_id,
                                         )
        product.product_image.save(name + '.jpg', ContentFile(input_file.getvalue()), save=False)
        product.save()
        print('Succes')
    except Exception as error:
        print(error)




print(cat_db)
