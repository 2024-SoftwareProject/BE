from django.contrib import admin
from .models import Post, Photo

# Post 모델을 관리자 페이지에 등록
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['postname', 'author', 'id']
    list_filter = ['author']
    search_fields = ['postname', 'contents']

# Photo 모델을 관리자 페이지에 등록
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['post', 'image_thumbnail', 'id']
    list_filter = []
    search_fields = ['post__postname']

    def image_thumbnail(self, obj):
        return obj.thumbnail()
    image_thumbnail.short_description = 'Thumbnail'
    image_thumbnail.allow_tags = True
