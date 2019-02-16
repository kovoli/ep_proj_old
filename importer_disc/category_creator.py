import os, sys
import django
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()
import random

from discounts.models import Category

import xmltodict
import json

with open('./cat_elektronika.xml') as fd:
    categories = xmltodict.parse(fd.read())

categories_list = categories['categories']['category']
print(len(categories_list))
count = 0
def parent_cat(parentid):
    for cat in categories_list:
        if cat['@id'] == parentid:
            return Category.objects.get(name=cat['#text'])


for category in categories['categories']['category']:
    #print(category)
    try:
        #parentid_name = categories_list[]
        if category['#text'] == 'Аксессуары':
            cat = Category.objects.create(name=category['#text'] + str(random.random()), parent=parent_cat(category['@parentId']))
            cat.save()
            count += 1
        else:
            cat = Category.objects.create(name=category['#text'], parent=parent_cat(category['@parentId']))
            cat.save()
            count += 1
        print(count)
    except Exception as a:
        print(a)

