from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.urls import reverse
from .models import Post, Photo
from .forms import PostForm, CommentForm
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Comment
from django.http import JsonResponse

def free_board(request):
    free_posts = Post.objects.filter(board_type="free_board")
    return render(request, 'main/free_board.html', {'posts': free_posts, 'board_type' : free_board})
def review_board(request):
    review_posts = Post.objects.filter(board_type="review_board")
    return render(request, 'main/review_board.html', {'posts': review_posts, 'board_type' : review_board})
def question_board(request):
    question_posts = Post.objects.filter(board_type="question_board")
    return render(request, 'main/question_board.html', {'posts': question_posts, 'board_type' : question_board})

# board.html 페이지를 부르는 board 함수
def board(request):
    postlist = Post.objects.all()
    return render(request, 'main/board.html',{'postlist':postlist})


# blog의 게시글(posting)을 부르는 posting 함수
def posting(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    post = Post.objects.get(pk=pk)
    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'main/posting.html', {'post':post}) #board_type 부분 추가 수정 

@login_required
def new_post(request, board_type=None):
    #board_type = request.GET.get('board_type')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user, board_type=board_type)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.board_type = board_type
            post.save()

            # 이미지를 업로드한 경우에만 실행
            if 'mainphotos' in request.FILES:
                # 이미지를 업로드한 경우에는 이미지를 저장하고 게시물을 저장
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
    #board_type = post.board_type
    #redirect_url = reverse('main/posting', kwargs={'board_type':board_type})
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
    