import os, sys, requests, io
import django
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()

import xml.etree.ElementTree as ET


from shop.models import Product, Price

def download_all_category_files():
    filename_list = []
    # 1. Бытовая техника
    # 2. Электроника
    categories_list = ['https://api.ozon.ru/PartnerTools/XmlFeed/11023170689840',
                       'https://api.ozon.ru/PartnerTools/XmlFeed/11023171038040']

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

# Скачивает все категории

succes_update = 0
succers_writes = 0
for file in download_all_category_files():
    tree = ET.parse('imports/' + file)
    root = tree.getroot()
    print(file)
    for prod in root.findall('.//offer'):
        product_data = {'name': None,
                        'vendorCode': 'null',
                        'barcode': None,
                        'price': None,
                        'oldprice': None,
                        'sales_notes': None,
                        'url': None
                        }
        try:
            for data in product_data.keys():
                if prod.find(data) is None:
                    continue
                elif data == 'url':
                    product_data[data] = 'https://f.gdeslon.ru/cf/0c7e8158ad?mid=12027&goto=' + prod.find(data).text[:prod.find(data).text.index('?')]
                else:
                    product_data[data] = prod.find(data).text
            get_product = None
            try:
                get_product = Product.objects.get(name=product_data['name'])
            except:
                succers_writes
            try:
                if product_data['vendorCode'] != None:
                    get_product = Product.objects.get(vendorCode=product_data['vendorCode'])
            except:
                succers_writes
            try:
                if product_data['barcode'] != None:
                    get_product = Product.objects.get(barcode=product_data['barcode'])
            except:
                succers_writes

            if get_product != None:
                del product_data['vendorCode']
                del product_data['barcode']
                product_data['shop_id'] = 1
                try:
                    price_curent = get_product.prices.get(shop_id=1)
                    price_curent.price = product_data['price']
                    price_curent.oldprice = product_data['oldprice']
                    price_curent.name = product_data['name']
                    price_curent.sales_notes = product_data['sales_notes']
                    price_curent.url = product_data['url']
                    price_curent.save()
                    get_product.save()
                    succes_update += 1
                except Price.DoesNotExist:
                    get_price_shop = get_product.prices.create(**product_data)
                    get_product.save()
                    succers_writes += 1
        except Exception as error:
            print(error)

print('Всего товаров', len(root.findall('.//offer')))
print('Цен созданно', succers_writes)
print('Цен обновленно', succes_update)

