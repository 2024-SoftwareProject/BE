from django.urls import path
from .views import *
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView

app_name='board_app'

urlpatterns=[
    path('admin/', admin.site.urls),
    path('', board, name='board'), 

    path('free_board/', free_board, name='free_board'),
    path('<str:board_type>/new_post/', new_post, name='new_post'), #<str:board_type>, name='free_board_new_post
    path('free_board/<int:pk>/remove/', remove_post, name="free_board_remove_posting"),
    path('free_board/<int:pk>/', posting, name="free_board_posting"), #free_board_posting
    path('<str:board_type>/<int:pk>/edit', edit_post, name="edit_post"),
    path('free_board/<int:pk>/add_comment/', add_comment, name='free_board_add_comment'),
    path('<str:board_type>/<int:pk>/edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),# 수정 <str:board_type>
    path('free_board/<int:pk>/delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('<str:board_type>/add_to_scrap/<int:pk>/', add_to_scrap,name='add_to_scrap'),
    path('<str:board_type>/remove_from_scrap/<int:pk>/', remove_from_scrap, name='remove_from_scrap'),

    path('review_board/', review_board, name='review_board'),
    path('review_board/<int:pk>/remove/', remove_post, name="review_board_remove_posting"),
    path('review_board/<int:pk>/', posting, name="review_board_posting"), 
    path('review_board/<int:pk>/edit', edit_post, name="review_board_edit_post"),
    path('review_board/<int:pk>/add_comment/', add_comment, name='review_board_add_comment'),


    path('question_board/', question_board, name='question_board'),
    path('question_board/<int:pk>/remove/', remove_post, name="question_board_remove_posting"),
    path('question_board/<int:pk>/', posting, name="question_board_posting"), 
    path('question_board/<int:pk>/edit', edit_post, name="question_board_edit_post"),
    path('question_board/<int:pk>/add_comment/', add_comment, name='question_board_add_comment'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)