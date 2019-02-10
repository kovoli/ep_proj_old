import os, sys, requests, io, re
import django
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()

import xml.etree.cElementTree as ET


from shop.models import Product, Category, Vendor, Price

# For images
from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen

cat_db = Category.objects.values('id', 'name')

def check_field_not_none(field):
    if field is not None:
        return field
    else:
        return None


# Helper Functions
def description_beautify(text):
    if text == None:
        return 'С подробным описанием товара и ценами можно ознакомиться на сайте продавца.'
    else:
        regex = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\:)\s"
        subst = "</br>"
        return re.sub(regex, subst, text, 0, re.MULTILINE)


def param_dict(param):
    param_dict = {}
    for par in param:
        if 'unit' in par.attrib:
            param_dict[par.attrib['name']] = [par.text, par.attrib['unit']]
        else:
            param_dict[par.attrib['name']] = [par.text]
    return param_dict


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
        if off.find(data) is None:
            continue
        if data == 'url':
            offer_price_data[data] = 'https://f.gdeslon.ru/cf/0c7e8158ad?mid=12027&goto=' + off.find(data).text[:off.find(data).text.index('?')]
        else:
            offer_price_data[data] = off.find(data).text

    return Price.objects.create(**offer_price_data)


def video_rewiew_param(param):
    youtube_url = 'https://www.youtube.com/embed/'
    for par in param:
        if par.attrib['name'] == 'Видеообзор':
            a = par.text
            return youtube_url + a[a.index('=') + 1:]
    return None


def download_all_category_files():
    filename_list = []
    # 1. Бытовая техника
    # 2. Электроника
    categories_list = ['https://api.ozon.ru/PartnerTools/XmlFeed/11023172898280',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023172901410',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023172904400',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023172908700',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023172905810',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023172890790',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023172909700',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023172908100',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023177883650',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023172902130',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023172899000',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023172901540',
                       ]

    url = 'https://api.ozon.ru/AuthServer/Token'
    data = {'grant_type': 'password', 'username': 'kovoli1985@gmail.com', 'password': 'Mafusal1985!'}
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


succers_writes = 0
error_count = 0
for file in download_all_category_files():
    tree = ET.parse('imports/' + file)
    root = tree.getroot()
    categories = root.findall('.//category')
    print('Всего товаров', len(root.findall('.//offer')))
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
                    product_data[data] = param_dict(off.findall(data))
                elif data == 'categoryId':
                    del product_data['categoryId']
                    product_data['category_id'] = def_category(off.find(data).text)
                else:
                    product_data[data] = off.find(data).text

            vendor = vendor_get_or_create(off.find('vendor').text)
            video = video_rewiew_param(off.findall('param'))
            original_picture = check_field_not_none(off.find('picture').text)
            input_file = BytesIO(urlopen(original_picture, ).read())

            product = Product.objects.create(**product_data)
            product.vendor = vendor
            product.video = video
            add_price_to_product(off, product)

            product.product_image.save(product_data['name'] + '.jpg', ContentFile(input_file.getvalue()), save=False)
            product.save()
            succers_writes += 1

        except Exception as error:
            error_count += 1


print('Сделанно записей', succers_writes)
print('Всего товаров', len(root.findall('.//offer')))
print('Ошибок', error_count)
