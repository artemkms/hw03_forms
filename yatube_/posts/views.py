from django.shortcuts import render, get_object_or_404
from .models import Group, Post
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model


User = get_user_model()


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page_obj': page_obj,
        'title': 'Последние обновления на сайте',
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile_posts = user.posts.order_by('-pub_date')
    paginator = Paginator(profile_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/profile.html'
    context = {
        'page_obj': page_obj,
        'user': user,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_count = Post.objects.filter(author=post.author).count()
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'post_count': post_count,
    }
    return render(request, template, context)
