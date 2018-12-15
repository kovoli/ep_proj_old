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

#for i in categories:
    #print(i.attrib['id'])


# По ID находит название категории
#a = root.find(".//category[@id='1177087']")
#print(a.text)

cat_db = Category.objects.values('id', 'name')


# Helper Functions
def description_beautify(text):
    regex = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\:)\s"
    subst = "</br>"
    return re.sub(regex, subst, text, 0, re.MULTILINE)


def parameter_beatify():  # TODO: Доделать функцию характеристики
    pass


def def_category(category_id):
    id_cat_name = root.find(".//category[@id='{}']".format(category_id))
    print(id_cat_name.text)
    id_cat_name = id_cat_name.text
    for i in Category.objects.values('id', 'name'):
        if i['name'] == id_cat_name:
            return i['id']





print(len(root.find('.//offers')))

for offer in root.findall('.//offer'):
    try:
        name = offer.find('name').text
        description = description_beautify(offer.find('description').text)
        param = offer.findall('param')
        characteristic = []
        for par in param:
            characteristic.append('<li>' + par.attrib['name'] + ': ' + par.text + '</li>')
        characteristic = ''.join(characteristic)
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
print(find_cat_name_by_id_xml_vendor('1181156'))