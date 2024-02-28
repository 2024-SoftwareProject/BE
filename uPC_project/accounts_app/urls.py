from django.urls import path
from . import views

urlpatterns=[
    path('signup/', views.signup.as_view(), name='signup'),
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/update_account/', views.update_account, name='update_account'),
    path('mypage/delete_account/', views.delete_account , name='delete_account'),

    path('agreement/', views.Agreement.as_view(), name='agreement'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
    
]