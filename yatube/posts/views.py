from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .utils import get_page_context
from .models import Group, Post, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    context = {
        'page_obj': get_page_context(post_list, request),
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    context = {
        'group': group,
        'page_obj': get_page_context(post_list, request),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    context = {'page_obj': get_page_context(post_list, request),
               'author': author,
               }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', request.user)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post.pk,)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post.save()
        return redirect('posts:post_detail', post.pk,)
    is_edit = True
    context = {'form': form, 'is_edit': is_edit}
    return render(request, 'posts/create_post.html', context)
