from django.urls import path
from . import views

app_name = 'products_app'

urlpatterns = [
    # path("", views.test, name="test"),
    path('', views.search_view, name='search'),
    path('report/', views.search_report_view, name='search_report'),
]