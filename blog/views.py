from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostModelForm, PostForm, CommentModelForm


# Comment 승인
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


# Comment 삭제
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


# Comment 등록
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # form 객체생성
        form = CommentModelForm(request.POST)
        # form valid check
        if form.is_valid():
            # author, text 값이 comment 객체에 저장
            comment = form.save(commit=False)
            # comment 객체에 매칭되는 post id를 저장
            comment.post = post
            # DB에 저장됨
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentModelForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


# Post 삭제
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


# Post 수정
@login_required
def post_edit(request, pk):
    # DB에 해당 pk와 매칭되는 Post 객체를 가져온다
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # Form 데이터를 입력하고 등록요청버튼 Save 클릭 시
        form = PostModelForm(request.POST)
        # Form 데이터가 clean 한 상태 (조건에 다 만족할 때)
        if form.is_valid():
            # DB에 저장하지 않은 상태로 post 객체에 넣어둠 (author,published_date 값 지정해주기위해 잠시 멈춤)
            # title, text 필드의 값이 저장이 된다.
            post = form.save(commit=False)
            post.author = User.objects.get(username=request.user.username)
            post.published_date = timezone.now()
            # DB에 등록됨
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # 수정하기 전에 데이터 읽어옴
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


# Post 등록
@login_required
def post_new(request):
    if request.method == 'POST':
        # Form 데이터를 입력하고 등록요청버튼 Save 클릭 시
        form = PostForm(request.POST)
        # Form 데이터가 clean 한 상태 (조건에 다 만족할 때)
        if form.is_valid():
            print(form.cleaned_data)
            post = Post.objects.create(author=User.objects.get(username=request.user.username), published_date=timezone.now(), title=form.cleaned_data['title'],
                                       text=form.cleaned_data['text'])
            # DB에 저장하지 않은 상태로 post 객체에 넣어둠 (author,published_date 값 지정해주기위해 잠시 멈춤)
            # title, text 필드의 값이 저장이 된다.
            # post = form.save(commit=False)
            # post.author = User.objects.get(username=request.user.username)
            # post.published_date = timezone.now()
            # # DB에 등록됨
            # post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # 등록 Form 보여주는 GET 방식
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


# Post 상세조회
def post_detail(request, pk):
    # get_object_or_404(모델명, primary key )
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# Post 목록 조회
def post_list(request):
    # name = 'Django'
    # return HttpResponse('''<h2>Post List</h2>
    #     <p>Welcome, {name}님!!</p><p>{content}</p>'''.format(name=name, content=request.user))

    # QuerySet을 사용하여 DB에서 Post 목록 가져오기
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts})
