import os, sys
import django
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()

import xml.etree.ElementTree as ET


from shop.models import Product, Price


tree = ET.parse('xml_imports/10500.xml')
root = tree.getroot()



succers_writes = 0
asc = 0
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
            print('not')
        try:
            if product_data['vendorCode'] != None:
                get_product = Product.objects.get(vendorCode=product_data['vendorCode'])
        except:
            print('not')
        try:
            if product_data['barcode'] != None:
                get_product = Product.objects.get(barcode=product_data['barcode'])
        except:
            print('not')

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
                print('Succes')
                succers_writes += 1
            except Price.DoesNotExist:
                asc += 1
                print(asc)
                get_price_shop = get_product.prices.create(**product_data)
                get_product.save()
                print('Succes')
                succers_writes += 1
    except Exception as error:
        print(error)

print(succers_writes)
print(asc)
print(len(root.findall('.//offer')))