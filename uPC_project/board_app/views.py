from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.urls import reverse
from .models import Post, Photo, Scrap
from .forms import PostForm, CommentForm
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Comment
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

def free_board(request):
    free_posts = Post.objects.filter(board_type="free_board")
    return render(request, 'main/free_board.html', {'posts': free_posts, 'board_type' : free_board})
def review_board(request):
    review_posts = Post.objects.filter(board_type="review_board")
    return render(request, 'main/review_board.html', {'posts': review_posts, 'board_type' : review_board})
def question_board(request):
    question_posts = Post.objects.filter(board_type="question_board")
    return render(request, 'main/question_board.html', {'posts': question_posts, 'board_type' : question_board})

def board(request):
    postlist = Post.objects.all()
    return render(request, 'main/board.html',{'postlist':postlist})


def posting(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'main/posting.html', {'post':post}) #board_type 부분 추가 수정 

@login_required
def new_post(request, board_type=None):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user, board_type=board_type)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.board_type = board_type
            post.save()

            # 이미지를 업로드한 경우에만 실행
            if 'mainphotos' in request.FILES:
                for img in request.FILES.getlist('mainphotos'):
                    Photo.objects.create(post=post, image=img)
            if board_type == 'free_board':
                return redirect('board_app:free_board')
            elif board_type == 'review_board':
                return redirect('board_app:review_board')
            elif board_type == 'question_board':
                return redirect('board_app:question_board')
            #return redirect('/board/')
    else:
        form = PostForm(user=request.user, board_type=board_type)
    return render(request, 'main/new_post.html', {'form': form,'board_type': board_type})


@login_required
def remove_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission to remove this comment.")
    
    if request.method == 'POST': 
        post.delete()
        return redirect('/board/')
    return render(request, 'main/remove_post.html', {'Post': post})

@login_required
def edit_post(request, pk, board_type): 
    post = get_object_or_404(Post, pk=pk)
    photos = post.photos.all()

    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission to edit this post.")
    
    if request.method == 'POST':
        # POST 요청이면 폼을 생성하고 유효성을 검사
        form = PostForm(request.POST, request.FILES, instance=post, user=request.user, board_type=board_type)
        if form.is_valid():
            # 폼을 저장하여 게시물을 업데이트
            updated_post = form.save(commit=False)
            updated_post.author = request.user
            updated_post.board_type = board_type
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

            # 수정한 게시물의 상세 페이지로 이동
            if updated_post.board_type == 'free_board':
                return HttpResponseRedirect(reverse('board_app:free_board_posting', args=(pk,)))
            elif updated_post.board_type == 'review_board':
                return HttpResponseRedirect(reverse('board_app:review_board_posting', args=(pk,)))
            elif updated_post.board_type == 'question_board':
                return HttpResponseRedirect(reverse('board_app:question_board_posting', args=(pk,)))

    else:
        form = PostForm(instance=post, user=request.user)

    return render(request, 'main/edit_post.html', {'form': form, 'photos': photos, 'board_type': board_type})


@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        content = request.POST.get('content')
        author = request.user
        post = get_object_or_404(Post, pk=pk)
        board_type = request.POST.get('board_type')
        Comment.objects.create(post=post, author=author, content=content)
        if board_type == 'free_board':
            return redirect('board_app:free_board_posting', pk=post.pk)
        elif board_type == 'review_board':
            return redirect('board_app:review_board_posting', pk=post.pk)
        elif board_type == 'question_board':
            return redirect('board_app:question_board_posting', pk=post.pk)

        

@login_required
def edit_comment(request, pk, comment_id, board_type):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = comment.post
    if comment.author != request.user:
        return HttpResponseForbidden("You don't have permission to edit this comment.")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            # 수정된 댓글을 보는 원래 게시물의 페이지로 리다이렉트
            if board_type == 'free_board':
                return redirect('board_app:free_board_posting', pk=post.pk)
            elif board_type == 'review_board':
                return redirect('board_app:review_board_posting', pk=post.pk)
            elif board_type == 'question_board':
                return redirect('board_app:question_board_posting', pk=post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'main/posting.html', {'form': form, 'pk': pk, 'comment_id': comment_id})


@login_required
def delete_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        return JsonResponse({'message': '댓글이 삭제되었습니다.', 'status': 'success'})
    else:
        return HttpResponseForbidden("You don't have permission to delete this comment.")
    
@login_required
def add_to_scrap(request, pk, board_type):
    post = Post.objects.get(id=pk)
    scrap, created = Scrap.objects.get_or_create(user=request.user)
    board_type =post.board_type
    if post in scrap.posts.all():
        scrap.posts.remove(post)
        message = '게시물이 찜 목록에서 제거되었습니다.'
        is_scraped = False
    else:
        scrap.posts.add(post)
        message = '게시물이 찜 목록에 추가되었습니다.'
        is_scraped = True
    
    messages.success(request, message)

    return JsonResponse({'message': message, 'is_scraped': is_scraped})

@login_required
def toggle_scrap(request, board_type, pk):
    post = get_object_or_404(Post, pk=pk)
    try:
        scrap = request.user.scrap
    except Scrap.DoesNotExist:
        scrap = Scrap.objects.create(user=request.user)

    if scrap.is_post_scrap(pk):
        scrap.remove_from_scrap(post)  
        message = '게시물이 찜 목록에서 제거되었습니다.'
        is_scraped = False
    else:
        scrap.add_to_scrap(post)
        message = '게시물이 찜 목록에 추가되었습니다.'
        is_scraped = True

    return JsonResponse({'message': message, 'is_scraped': is_scraped})


@login_required
def check_post_scrap(request, pk, board_type): 
    post = get_object_or_404(Post, pk=pk) 
    scrap_exists = request.user.scrap.is_post_scrap(pk) if hasattr(request.user, 'scrap') else False
    return JsonResponse({'is_post_scrap': scrap_exists})

@login_required
@require_http_methods(["GET"])  # GET 요청만 허용
def scrap_status(request, board_type, pk):
    # 사용자가 해당 게시물을 찜했는지 여부를 확인
    try:
        scrap = Scrap.objects.get(user=request.user, posts=pk)
        is_scraped = True
    except Scrap.DoesNotExist:
        is_scraped = False
    return JsonResponse({'is_scraped': is_scraped})