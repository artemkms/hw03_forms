from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, User
from .test_urls import const_urls, half_const_urls


class FormCreateTest(TestCase):
    non_const_urls ={
        'post_edit': 'posts:post_edit'
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        author = User.objects.create_user(username='CanEdit')
        author.save()
        test_post = Post.objects.create(
            text='Тестовый Текст',
            author=author,
        )

    def setUp(self):
        self.user = User.objects.get(username='CanEdit')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Новый пост',
            'author': User.objects.get(username='CanEdit'),
        }
        self.authorized_client.post(
            reverse(const_urls['create']),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Post.objects.count(), posts_count + 1,
                         'Запись не доавлена в базу данных')
        form_data = {
            'text': 'Новый текст',
            'author': User.objects.get(username='CanEdit'),
        }
        test_post_id = Post.objects.get(text='Тестовый Текст').id
        self.authorized_client.post(
            reverse(self.non_const_urls['post_edit'],
                    kwargs={'post_id': test_post_id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.get(pk=test_post_id).text, 'Новый текст',
                         'Запись не изменена')
