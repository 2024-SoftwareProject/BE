from products_app.models import Product
from django.db import models

def get_products_by_latest(query, min=0, max=3000000):
    products = Product.objects.filter(Pd_Category=query, Pd_Price__range=(min, max)).order_by('Pd_IndexNumber')
    return products

def get_products_by_price_low(query, min=0, max=3000000):
    products = Product.objects.filter(Pd_Category=query,Pd_Price__range=(min, max)).order_by('Pd_Price')
    return products

def get_products_by_price_high(query, min=0, max=3000000):
    products = Product.objects.filter(Pd_Category=query,Pd_Price__range=(min, max)).order_by('-Pd_Price')
    return products

def get_products_by_popularity(query, min=0, max=3000000):
    products = Product.objects.filter(Pd_Category=query, Pd_Price__range=(min, max)).order_by('-Pd_Count')
    return products
