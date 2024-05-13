from .models import CategoryProduct
from .models import Category
from django.db import models

from products_app.models import Product

def get_products_by_latest(categoryNumber, min=0, max=3000000, aOption='abcdef9129', bOption='abcdef9129', cOption='abcdef9129', dOption='abcdef9129', eOption='abcdef9129'):
    print(aOption)
    print("gaga")
    products = list(CategoryProduct.objects.filter(Pd_Category__icontains=aOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max)))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=bOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=cOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=dOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=eOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))

    sorted_products = sorted(products, key=lambda x: x.Pd_IndexNumber)
    
    return sorted_products


def get_products_by_price_low(categoryNumber, min=0, max=3000000, aOption='abcdef9129', bOption='abcdef9129', cOption='abcdef9129', dOption='abcdef9129', eOption='abcdef9129'):
    products = list(CategoryProduct.objects.filter(Pd_Name__icontains=aOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max)))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=bOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=cOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=dOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=eOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))

    sorted_products = sorted(products, key=lambda x: x.Pd_Price)
    
    return sorted_products


def get_products_by_price_high(categoryNumber, min=0, max=3000000, aOption='abcdef9129', bOption='abcdef9129', cOption='abcdef9129', dOption='abcdef9129', eOption='abcdef9129'):
    print(aOption)
    products = list(CategoryProduct.objects.filter(Pd_Name__icontains=aOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max)))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=bOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=cOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=dOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=eOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))

    
    print("gaga3")
    sorted_products = sorted(products, key=lambda x: -x.Pd_Price)
    
    return sorted_products


def get_products_by_popularity(categoryNumber, min=0, max=3000000, aOption='abcdef9129', bOption='abcdef9129', cOption='abcdef9129', dOption='abcdef9129', eOption='abcdef9129'):
    products = list(CategoryProduct.objects.filter(PPd_Name__icontains=aOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max)))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=bOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=cOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=dOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))
    products.extend(list(CategoryProduct.objects.filter(Pd_Name__icontains=eOption, Pd_CategoryNumber=categoryNumber, Pd_Price__range=(min, max))))

    sorted_products = sorted(products, key=lambda x: x.Pd_IndexNumber)
    
    return sorted_products

def get_all_products(categoryNumber, min=0, max=3000000):
    products = CategoryProduct.objects.filter(Pd_CategoryNumber=categoryNumber,Pd_Price__range=(min, max)).order_by('Pd_IndexNumber')
    return products

def plus_products_from_product_model(categoryNumber, categoryName):

    products = Product.objects.filter(Pd_Category__icontains=categoryName)
    
    # 가져온 데이터를 기반으로 새로운 객체 생성 및 저장
    for product in products:
        if not CategoryProduct.objects.filter(Pd_Name=product.Pd_Name).exists():
            category_product = CategoryProduct(
                Pd_Market=product.Pd_Market,
                Pd_CategoryNumber=categoryNumber,
                Pd_Category=product.Pd_Category,
                Pd_Name=product.Pd_Name,
                Pd_Price=product.Pd_Price,
                Pd_IMG=product.Pd_IMG,
                Pd_URL=product.Pd_URL,
                Pd_Count=product.Pd_Count
                # 필요한 경우 다른 필드들도 추가
            )
            category_product.save()

def get_minorname(categoryNumber):
    category = Category.objects.get(Ct_IndexNumber=categoryNumber)
    return category.Ct_MinorName