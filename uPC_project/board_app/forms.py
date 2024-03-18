from collections.abc import Iterable
from typing import Any, Mapping
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['postname', 'contents', 'mainphotos', 'author', 'board_type']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 사용자를 받아옴
        board_type = kwargs.pop('board_type', None)  # board_type을 kwargs에서 가져옴
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['board_type'].widget = forms.HiddenInput()
        if board_type is None and self.instance and self.instance.board_type:
            board_type = self.instance.board_type
        if board_type:  # post가 전달되었다면
            self.fields['board_type'].initial = board_type  # board_type 필드의 초기값 설정
        if user:
            self.instance.author = user  # 현재 로그인한 사용자를 작성자로 설정
            self.fields['author'].widget = forms.HiddenInput()  # 작성자 필드를 숨김

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        if commit:
            self.save_m2m()
        return instance
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글 내용'
        }