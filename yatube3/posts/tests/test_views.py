from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from ..models import Post, Group

User = get_user_model()

class PostViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TrueName')
        cls.group = Group.objects.create(
            title='test-title',
            description='test-description',
            slug='test-slug'
        )
        for i in range(1, 13):
            cls.post = Post.objects.create(
                author=cls.user,
                group=cls.group,
                text='test-text' + str(i),
                pub_date='04.02.2022'
            )

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def check_post_in_page(self, url, text, user, group):
        response = self.authorized_client.get(url)
        self.assertEqual(self.post.text, 'test-text12')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.group, self.group)

    def test_post_appears_on_pages(self):

        self.group1 = Group.objects.create(title="test", slug="test1")

        self.post2 = Post.objects.create(
            text='Test text',
            author=self.user,
            group=self.group1
        )

        urls = (reverse('posts:index'),
                reverse('posts:profile', kwargs={'username': 'TrueName'}),
                reverse('posts:group_posts', kwargs={'slug': 'test-slug'}),
                )

        for url in urls:
            with self.subTest(url=url):
                self.check_post_in_page(url, 'Test text', self.user,
                self.group1
                )


    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_posts', kwargs={'slug': 'test-slug'}),
            'posts/profile.html': reverse('posts:profile', kwargs={'username': 'TrueName'}),
            'posts/post_detail.html': reverse('posts:post_detail', kwargs={'post_id': '1'}),
            'posts/post_create.html': reverse('posts:post_create'),
            'posts/post_create.html': reverse('posts:post_edit', kwargs={'post_id': '1'}),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

        
    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(
            response.context['page_obj'][0], self.post
        )

    def test_group_posts_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:group_posts', kwargs={'slug': 'test-slug'}
        ))
        self.assertEqual(
            response.context['page_obj']
            [0].author.username,
            'TrueName'
        )
        self.assertEqual(
            response.context['page_obj']
            [0].text,
            'test-text12'
        )
        self.assertEqual(
            response.context['page_obj']
            [0].group.title,
            'test-title'
        )
        self.assertEqual(response.context['group'], self.group)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': 'TrueName'}
        ))
        self.assertEqual(
            response.context['page_obj']
            [0].author.username,
            'TrueName'
        )
        self.assertEqual(
            response.context['page_obj']
            [0].text,
            'test-text12'
        )
        self.assertEqual(
            response.context['page_obj']
            [0].group.title,
            'test-title'
        )
        self.assertEqual(response.context['author'], self.user)

    def test_post_detail_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': '12'}
        ))
        self.assertEqual(response.context['post'], self.post)

    def test_post_create_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField
        }        
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': '1'}
        ))
        form_fields = {
            'text': forms.fields.CharField
        }        
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    class PaginatorViewsTest(TestCase):
        def test_first_page_index_contains_ten_records(self):
            response = self.client.get(reverse('index'))
            self.assertEqual(len(response.context['object_list']), 10)

        def test_second_page_index_contains_three_records(self):
            response = self.client.get(reverse('index') + '?page=2')
            self.assertEqual(len(response.context['object_list']), 3)

        def test_first_page_group_posts_contains_ten_records(self):
            response = self.client.get(reverse('posts:group_posts')) 
            self.assertEqual(len(response.context['object_list']), 10)

        def test_second_page_group_posts_contains_three_records(self):
            response = self.client.get(reverse('posts:group_posts') + '?page=2')
            self.assertEqual(len(response.context['object_list']), 3)

        def test_first_page_profile_contains_ten_records(self):
            response = self.client.get(reverse('posts:profile'))
            self.assertEqual(len(response.context['object_list']), 10)

        def test_second_page_profile_contains_three_records(self):
            response = self.client.get(reverse('posts:profile') + '?page=2')
            self.assertEqual(len(response.context['object_list']), 3)


