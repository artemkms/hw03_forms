from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User

from http import HTTPStatus


const_urls = {
    'index': 'posts:index',
    'author': 'about:author',
    'tech': 'about:tech',
    'create': 'posts:post_create'
}

half_const_urls = {
    'group_posts': 'posts:group_posts',
    'profile': 'posts:profile',
}


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_homepage(self):
        # Делаем запрос к главной странице и проверяем статус
        response = self.guest_client.get(reverse(const_urls['index']))
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about(self):
        response = self.guest_client.get(reverse(const_urls['author']))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech(self):
        response = self.guest_client.get(reverse(const_urls['tech']))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class PostsURLTest(TestCase):
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
            text='Тестовый Текст',
            author=author,
            group=Group.objects.get(title='TestGroup'),
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)
        # Создаём клиент для пользователя, который создаёт
        # и редактирует пост
        self.authorized_client_edit = Client()
        # Создаём пользователя, который создаёт и может редактировать пост
        self.user_edit = User.objects.get(username='CanEdit')
        # Авторизуем его
        self.authorized_client_edit.force_login(self.user_edit)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/TestSlug/': 'posts/group_list.html',
            '/profile/CanEdit/': 'posts/profile.html',
            f"/posts/{Post.objects.get(text='Тестовый Текст').id}/":
                'posts/post_detail.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client_edit.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_post_edit_author(self):
        """URL-адрес редактирования поста доступен его автору"""
        address = f"/posts/{Post.objects.get(text='Тестовый Текст').id}/edit/"
        response = self.authorized_client_edit.get(address)
        self.assertEqual(
            response.status_code, HTTPStatus.OK,
            'Страница редактирования поста недоступна автору поста'
        )

    def test_urls_post_edit(self):
        """URL-адрес редактирования поста перенаправляет на страницу
        поста пользователя, который не является его автором"""
        address = f"/posts/{Post.objects.get(text='Тестовый Текст').id}/edit/"
        response = self.authorized_client.get(address, follow=True)
        self.assertRedirects(response,
                             f"/posts/{Post.objects.get(text='Тестовый Текст').id}/")

    def test_urls_create_post_unauthorised_user(self):
        """URL-адрес страницы создания поста перенаправляет
        неавторизованного пользователя на страницу входа"""
        address = '/create/'
        response = self.guest_client.get(address, follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_urls_unexisting_page(self):
        """URL-адрес несущетсвующей страницы возвращает ошибку 404"""
        address = '/unexisting_page/'
        response = self.authorized_client.get(address)
        self.assertEqual(
            response.status_code, HTTPStatus.NOT_FOUND,
            'URL-адрес несущетсвующей страницы не возвращает ошибку 404'
        )

    def test_urls_status_codes_unauthorised_user(self):
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/TestSlug/': 'posts/group_list.html',
            '/profile/CanEdit/': 'posts/profile.html',
            f"/posts/{Post.objects.get(text='Тестовый Текст').id}/":
                'posts/post_detail.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
