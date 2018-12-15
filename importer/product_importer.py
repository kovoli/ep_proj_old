import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()

import xml.etree.ElementTree as ET


from shop.models import Product, Category

from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen

tree = ET.parse('1133722.xml')
root = tree.getroot()

categories = root.findall('.//category')

#for i in categories:
    #print(i.attrib['id'])


# По ID находит название категории
#a = root.find(".//category[@id='1177087']")
#print(a.text)

cat_db = Category.objects.values('id', 'name')

def find_cat_name_by_id_xml_vendor(id_cat):
    id_cat_name = root.find(".//category[@id='{}']".format(id_cat))
    return id_cat_name.text
# Получаю насвание категории


def def_category(category_id):
    for i in cat_db:
        if i['name'] == category_id:
            return i['id']

print(len(root.find('.//offers')))

for offer in root.findall('.//offer'):
    try:
        name = offer.find('name').text
        description = offer.find('description').text
        param = offer.findall('param')
        characteristic = []
        for par in param:
            characteristic.append('<li>' + par.attrib['name'] + ': ' + par.text + '</li>')
        characteristic = ''.join(characteristic)
        barcode = offer.find('barcode').text
        vendorCode = offer.find('vendorCode').text

        categoriya = offer.find('categoryId').text
        cat2 = find_cat_name_by_id_xml_vendor(categoriya)
        category_id = def_category(cat2)
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