from django.urls import path
from .views import *
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

app_name='board_app'

urlpatterns=[
    path('admin/', admin.site.urls),
    path('', board, name='board'), #board/
    path('new_post/', new_post),  
    path('<int:pk>/remove/', remove_post, name="remove_posting"),
    path('<int:pk>/', posting, name="posting"), 
    path('<int:pk>/edit', edit_post, name="edit_post"), 
    path('<int:pk>/add_comment/', add_comment, name='add_comment'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)