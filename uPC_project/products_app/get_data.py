from products_app.models import Product

def get_products_by_category(query):
    products = Product.objects.filter(Pd_Category=query)
    return products


def get_products_by_price_asc(query):
    products = Product.objects.filter(Pd_Category=query).order_by('Pd_Price')
    return products