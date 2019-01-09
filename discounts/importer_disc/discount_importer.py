import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()

import xml.etree.ElementTree as ET

from discounts.models import DiscountProduct, Category, Vendor

# For images
from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen

import re

