from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from ..models import Post, Group, User
from .test_urls import const_urls, half_const_urls


class PostsPagesTests(TestCase):
    non_const_urls = {
        'post_detail': 'posts:post_detail',
        'post_edit': 'posts:post_edit'
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title='TestGroup',
            slug='TestSlug',
            description='Test'
        )
        author = User.objects.create_user(username='CanEdit')
        author.save()
        Post.objects.create(
            text='Тестовый Текст Тест views',
            author=author,
            group=Group.objects.get(title='TestGroup')
        )

    def setUp(self):
        # Создаем авторизованный клиент
        self.user = User.objects.get(username='CanEdit')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            reverse(const_urls['index']): 'posts/index.html',
            reverse(half_const_urls['group_posts'],
                    kwargs={'slug': 'TestSlug'}): 'posts/group_list.html',
            reverse(half_const_urls['profile'],
                    kwargs={'username': 'CanEdit'}): 'posts/profile.html',
            reverse(self.non_const_urls['post_detail'],
                    kwargs={'post_id': Post.objects.get(text='Тестовый Текст Тест views').id}):
                'posts/post_detail.html',
            reverse(self.non_const_urls['post_edit'],
                    kwargs={'post_id': Post.objects.get(text='Тестовый Текст Тест views').id}):
                'posts/create_post.html',
            reverse(const_urls['create']): 'posts/create_post.html'
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class PaginatorViewsTest(TestCase):
    """Тест Paginator"""

    @classmethod
    def setUpClass(cls):
        """Создаём группу и 16 постов"""
        super().setUpClass()
        Group.objects.create(
            title='TestGroup',
            slug='TestSlug',
            description='Test'
        )
        author = User.objects.create_user(username='CanEdit')
        author.save()
        # первый пост не имеет группы
        Post.objects.create(
            text='Текст первого поста',
            author=author
        )
        for i in range(2, 17):
            Post.objects.create(
                text=f'Текст поста номер {i}',
                author=author,
                group=Group.objects.get(slug='TestSlug')
            )

    def setUp(self):
        """Создаем авторизованный клиент"""
        self.user = User.objects.get(username='CanEdit')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        """Проверка: количество постов на первой странице равно 10."""
        response = self.authorized_client.get(reverse(const_urls['index']))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_six_records(self):
        """Проверка: на второй странице должно быть шесть постов."""
        response = self.authorized_client.get(reverse(const_urls['index'])
                                              + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 6)

    def test_first_page_TestGroup_contains_ten_records(self):
        """Проверка: количество постов на первой странице равно 10."""
        response = self.authorized_client.get(reverse(
            half_const_urls['group_posts'], kwargs={'slug': 'TestSlug'})
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_TestGroup_contains_five_records(self):
        """Проверка: количество постов на второй странице равно 5."""
        response = self.authorized_client.get(
            reverse(half_const_urls['group_posts'], kwargs={'slug': 'TestSlug'})
            + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_first_page_profile_CanEdit_contains_ten_records(self):
        response = self.authorized_client.get(
            reverse(half_const_urls['profile'], kwargs={'username': 'CanEdit'}))
        # Проверка: количество постов на первой странице равно 10.
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_profile_CanEdit_contains_six_records(self):
        """Проверка: количество постов на второй странице равно 6."""
        response = self.authorized_client.get(
            reverse(half_const_urls['profile'], kwargs={'username': 'CanEdit'})
            + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 6)


class PostDetailTest(TestCase):
    """Тестируем view-функцию post_detail"""
    non_const_urls = {
        'post_detail': 'posts:post_detail',
        'post_edit': 'posts:post_edit'
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title='TestGroup',
            slug='TestSlug',
            description='Test'
        )
        author = User.objects.create_user(username='CanEdit')
        author.save()
        Post.objects.create(
            text='Тестовый Текст проверка',
            author=author,
        )

    def setUp(self):
        # Создаем авторизованный клиент
        self.user = User.objects.get(username='CanEdit')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_detail(self):
        """Проверка view-функции post_detail"""
        post = Post.objects.get(author=User.objects.get(username='CanEdit'))
        response = self.authorized_client.get(reverse(
            self.non_const_urls['post_detail'], kwargs={'post_id': Post.objects.get(
                text='Тестовый Текст проверка').id}))
        self.assertEqual(response.context['post'], post,
                         'Неправльно работает view-функия post_detail')

    def test_post_create_correct_context(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(const_urls['create']))
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)


class NewPost(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title='TestGroup',
            slug='TestSlug',
            description='Test'
        )
        author = User.objects.create_user(username='CanEdit')
        author.save()
        Post.objects.create(
            text='Тестовый Текст проверка',
            author=author,
            group=Group.objects.get(slug='TestSlug')
        )

    def setUp(self):
        # Создаем авторизованный клиент
        self.user = User.objects.get(username='CanEdit')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_index(self):
        response = self.authorized_client.get(reverse(const_urls['index']))
        posts = response.context.get('page_obj').object_list
        post = Post.objects.get(text='Тестовый Текст проверка')
        self.assertIn(post, posts,
                      'Поста нет на главной странице!')

    def test_new_post_group(self):
        response = self.authorized_client.get(
            reverse(half_const_urls['group_posts'], kwargs={'slug': 'TestSlug'})
        )
        posts = response.context.get('page_obj').object_list
        post = Post.objects.get(text='Тестовый Текст проверка')
        self.assertIn(post, posts,
                      'Поста нет на странице группы!')

    def test_new_post_profile(self):
        response = self.authorized_client.get(
            reverse(half_const_urls['profile'], kwargs={'username': 'CanEdit'})
        )
        posts = response.context.get('page_obj').object_list
        post = Post.objects.get(text='Тестовый Текст проверка')
        self.assertIn(post, posts,
                      'Поста нет на странице автора !')
