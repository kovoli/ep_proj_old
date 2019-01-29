import os, sys
import django
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()

import xml.etree.ElementTree as ET


from shop.models import Product, Price


tree = ET.parse('xml_imports/mvideo_products.xml')
root = tree.getroot()


succers_writes = 0
print(len(root.findall('.//offer')))
for prod in root.findall('.//offer'):

    product_data = {'name': None,
                    'price': None,
                    'url': None
                    }

    for data in product_data.keys():
        if data == 'name':
            if prod.find('model') != None:
                product_data['name'] = prod.find('name').text + ' ' + prod.find('model').text
            else:
                product_data['name'] = prod.find('name').text
        else:
            product_data[data] = prod.find(data).text

    get_product = None

    try:
        if prod.find('barcode').text != None:
            get_product = Product.objects.get(barcode=prod.find('barcode').text)
    except:
        try:
            if prod.find('model').text != None:
                get_product = Product.objects.get(vendorCode=prod.find('model').text)
        except:
            continue

    try:
        if get_product != None:
            product_data['shop_id'] = 2
            try:
                get_product.prices.get(shop_id=2).delete()
                get_price_shop = get_product.prices.create(**product_data)
                get_product.save()
                print('Succes')
                succers_writes += 1
            except Price.DoesNotExist:
                get_price_shop = get_product.prices.create(**product_data)
                get_product.save()
                print('Succes')
                succers_writes += 1
    except Exception as error:
        print(error)

print(succers_writes)
print(len(root.findall('.//offer')))