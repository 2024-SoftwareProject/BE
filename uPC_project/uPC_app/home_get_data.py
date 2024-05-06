from products_app.models import Product
from board_app.models import Post
from django.db import models

def get_products_by_popularity():
    products = Product.objects.order_by('-Pd_Count')[:5]
    return products

def get_posts():
    posts = posts = Post.objects.all().order_by('-id')[:5]

    return posts
