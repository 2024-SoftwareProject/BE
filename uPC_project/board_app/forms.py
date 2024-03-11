from collections.abc import Iterable
from typing import Any, Mapping
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postname', 'contents', 'mainphotos', 'author']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 사용자를 받아옴
        super(PostForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.author = user  # 현재 로그인한 사용자를 작성자로 설정
            self.fields['author'].widget = forms.HiddenInput()  # 작성자 필드를 숨김