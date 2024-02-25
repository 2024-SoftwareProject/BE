from django.urls import path
from . import views

urlpatterns=[
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('delete/', views.delete, name='delete'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('mypage/', views.mypage, name='mypage'),

]