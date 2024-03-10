from django.urls import path
from . import views

# app_name = 'products_app'

urlpatterns = [
    # path("", views.test, name="test"),
    path("", views.search_view, name='search'),
]