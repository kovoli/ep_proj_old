import os, sys
import django
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()

import xml.etree.ElementTree as ET


from shop.models import Product, Category, Vendor, Price


tree = ET.parse('xml_imports/10500.xml')
root = tree.getroot()


for prod in root.findall('.//offer'):
    product_data = {'name': None,
                    'vendorCode': 'null',
                    'barcode': None,
                    'price': None,
                    'oldprice': None,
                    'sales_notes': None
                    }
    try:
        for data in product_data.keys():
            if prod.find(data) is None:
                continue
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
            get_price_shop = get_product.prices.update(**product_data)
            get_product.save()
            print('Succes')
    except Exception as error:
        print(error)
