from django.db import models
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from PIL import Image

User = get_user_model()

# 게시글(Post)엔 제목(postname), 내용(contents)이 존재합니다
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    postname = models.CharField(max_length=50)
    contents = models.TextField()
    mainphotos = models.ManyToManyField('Photo',related_name='posts',blank=True)
    #board_type =models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.postname
    
    def delete(self, *args, **kwargs):
        # 게시물과 연결된 모든 사진을 가져옴
        photos = self.photos.all()
        # 사진을 모두 삭제
        for photo in photos:
            photo.delete()
        # 게시물 삭제
        super().delete(*args, **kwargs)

    BOARD_CHOICES = (
        ('free_board', '자유 게시판'),
        ('question_board', '질문 게시판'),
        ('review_board', '판매 게시판'),
    )
    board_type = models.CharField(max_length=20, choices=BOARD_CHOICES, null=True, blank=True)

class Photo(models.Model):
    post = models.ForeignKey(Post, related_name='photos', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def delete(self, *args, **kwargs):
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
            if os.path.exists(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def thumbnail(self):
        if self.image:
            return '<img src="{}" style="max-height:100px; max-width:100px;" />'.format(self.image.url)
        else:
            return '(No image)'
    thumbnail.allow_tags = True
    thumbnail.short_description = 'Thumbnail'

    def __str__(self):
        return f"Photo for {self.post.postname}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.content}'

class Scrap(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='scrap')
    posts = models.ManyToManyField('Post', related_name='scrapped_by', blank=True)

    def __str__(self):
        return f"{self.user}'s Scrap"

    def add_to_scrap(self, post):
        """
        사용자의 찜 목록에 게시물을 추가합니다.
        """
        self.posts.add(post)

    def remove_from_scrap(self, post):
        """
        사용자의 찜 목록에서 게시물을 제거합니다.
        """
        self.posts.remove(post)

    def is_post_scrapped(self, post):
        """
        게시물이 사용자의 찜 목록에 있는지 확인합니다.
        """
        return post in self.posts.all()