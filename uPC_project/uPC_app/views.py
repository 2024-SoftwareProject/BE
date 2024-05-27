from django.shortcuts import render
from django.http import HttpResponse

from products_app.models import Product
from board_app.models import Post
from . import home_get_data
from recommend_app.views import collaborative_filtering

def home(request):
    popularity_outputDB = home_get_data.get_products_by_popularity()
    post_outputDB = home_get_data.get_posts()
    
    recommended_products = []
    if request.user.is_authenticated:
        recommended_products = collaborative_filtering(request.user.id)

    return render(request, 'home.html', {
        'popularity_outputDB':popularity_outputDB ,
        'post_outputDB': post_outputDB,
        'recommended_products':recommended_products})

