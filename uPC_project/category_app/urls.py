from django.urls import path
from . import views

app_name = 'category_app'

urlpatterns = [
    path('', views.search_view, name='search'),
    path('report/', views.search_report_view, name='search_report'),

]
