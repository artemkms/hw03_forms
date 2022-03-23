from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Group, Post, User
from yatube.settings import posts_per_page


# Create your views here.
def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # В словаре context отправляем информацию в шаблон
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group.all()
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = group.title
    context = {
        'page_obj': page_obj,
        'group': group,
        'title': title
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    posts_count = author.posts.count
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
        'posts_count': posts_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    posts_count = author.posts.count
    title = f'Пост {post.text[:30]}'
    context = {
        'posts_count': posts_count,
        'post': post,
        'title': title
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user.username)
    groups = Group.objects.all()
    form = PostForm()
    title = 'Добавить запись'
    context = {
        'groups': groups,
        'form': form,
        'title': title
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    title = 'Редактировать запись'
    if not post.author == request.user:
        return redirect('posts:post_detail', post_id)
    else:
        post = Post.objects.get(pk=post_id)
        if request.method == 'POST':
            if form.is_valid():
                post.text = form.cleaned_data['text']
                post.group = form.cleaned_data['group']
                post.save()
                return redirect('posts:post_detail', post_id)
    form.text = post.text
    id = post_id
    context = {
        'form': form,
        'title': title,
        'id': id
    }
    return render(request, 'posts/create_post.html', context)
