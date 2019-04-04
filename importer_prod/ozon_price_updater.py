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
    # 3. Строительство и ремонт
    categories_list = ['https://api.ozon.ru/partner-tools.affiliates/XmlFeed/10500',
                       'https://api.ozon.ru/partner-tools.affiliates/XmlFeed/15500',
                       'https://api.ozon.ru/partner-tools.affiliates/XmlFeed/9700']

    url = 'https://api.ozon.ru/affiliates/partner-api/account/token'
    data = {'grant_type': 'password', 'email': 'kovoli1985@gmail.com', 'password': 'Mafusal1985!'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url=url, data=data, headers=headers)  # Делаю запрос
    convert_tocken = r.json()  # Получаю json c токеном
    # получаю токен
    tokken = {'token': convert_tocken["access_token"]}

    for cat_url in categories_list:
        # Запрос категории с токеном
        request_cat_catalog = requests.get(cat_url + '?token=' + tokken['token'])
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
errors = 0
not_found_barcode = 0
not_found_name = 0
for file in download_all_category_files():
    tree = ET.parse('imports/' + file)
    root = tree.getroot()
    print('Всего товаров', len(root.findall('.//offer')))
    for prod in root.findall('.//offer'):
        product_data = {'name': None,
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
                if product_data['barcode'] != None:
                    get_product = Product.objects.get(barcode=product_data['barcode'])
            except:
                not_found_barcode += 1
                try:
                    get_product = Product.objects.get(name=product_data['name'])
                except:
                    not_found_name += 1
                    continue

            if get_product != None:
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
            errors += 1

print('Цен созданно', succers_writes)
print('Цен обновленно', succes_update)
print('Ошибок', errors)
print('Не найденно barcode', not_found_barcode)
print('Не найденно название', not_found_name)

