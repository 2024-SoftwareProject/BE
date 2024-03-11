from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, Photo
from .forms import PostForm 
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Comment

# board.html 페이지를 부르는 board 함수
def board(request):
    postlist = Post.objects.all()
    return render(request, 'main/board.html',{'postlist':postlist})


# blog의 게시글(posting)을 부르는 posting 함수
def posting(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    post = Post.objects.get(pk=pk)
    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'main/posting.html', {'post':post})

def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # 이미지를 업로드한 경우에만 실행
            if 'mainphotos' in request.FILES:
                # 이미지를 업로드한 경우에는 이미지를 저장하고 게시물을 저장
                for img in request.FILES.getlist('mainphotos'):
                    Photo.objects.create(post=post, image=img)
            
            return redirect('/board/')
    else:
        form = PostForm(user=request.user)
    return render(request, 'main/new_post.html', {'form': form})

@login_required
def remove_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST': 
        post.delete()
        return redirect('/board/')
    return render(request, 'main/remove_post.html', {'Post': post})

@login_required
def edit_post(request, pk):
    # 게시물 객체를 가져옴
    post = get_object_or_404(Post, pk=pk)
    
    # 게시물에 연결된 모든 사진을 가져옴
    photos = post.photos.all()
    
    if request.method == 'POST':
        # POST 요청이면 폼을 생성하고 유효성을 검사
        form = PostForm(request.POST, request.FILES, instance=post, user=request.user)
        if form.is_valid():
            # 폼을 저장하여 게시물을 업데이트
            updated_post = form.save(commit=False)
            updated_post.author = request.user
            updated_post.save()

            # 삭제할 이미지를 가져와서 삭제
            if 'delete_photos' in request.POST:
                delete_ids = request.POST.getlist('delete_photos')
                for photo_id in delete_ids:
                    photo_to_delete = Photo.objects.get(id=photo_id)
                    photo_to_delete.delete()

            # 새로운 이미지를 추가
            for file in request.FILES.getlist('photos'):
                Photo.objects.create(post=updated_post, image=file)

            return HttpResponseRedirect(reverse('board_app:posting', args=(pk,)))
    else:
        # GET 요청이면 기존 게시물 데이터를 가지고 폼 생성
        form = PostForm(instance=post, user=request.user)

    return render(request, 'main/edit_post.html', {'form': form, 'photos': photos})

@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        content = request.POST.get('content')
        author = request.user
        post = get_object_or_404(Post, pk=pk)
        Comment.objects.create(post=post, author=author, content=content)
        return redirect('board_app:posting', pk=pk)
    