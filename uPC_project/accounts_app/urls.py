from django.urls import path
from . import views

urlpatterns=[
    
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),

    path('agreement/', views.Agreement.as_view(), name='agreement'),
    path('signup/', views.signup.as_view(), name='signup'),
    path('signupAuth/', views.signup_success, name='signup_success'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),

    path('recovery/pw/', views.recoveryPW.as_view(), name='recovery_pw'),
    path('recovery/pw/find/', views.ajax_find_pw, name='ajax_pw'),
    path('recovery/pw/auth/', views.auth_confirm, name='recovery_auth'),
    path('recovery/pw/reset/', views.auth_pw_reset, name='recovery_pw_reset'),

    path('mypage/', views.mypage, name='mypage'),
    path('mypage/updateAccount/', views.updateAccount, name='update_account'),
    path('mypage/deleteAccount/', views.deleteAccount , name='delete_account'),
    
]