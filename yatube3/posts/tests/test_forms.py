import shutil
import tempfile

from ..forms import PostForm
from ..models import Post, Group
from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

User = get_user_model()


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Name')
        cls.group = Group.objects.create(
            title='test-title',
            slug='test-slug',
            description='test-description'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='post-test-text'
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        posts_count = Post.objects.count()  
        form_data = {
            'text': 'test-text',
            'group': self.group
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            {'text': 'test-text',
            'group': '1'},
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': 'Name'}))
        self.assertEqual(Post.objects.count(), posts_count+1)
        self.assertTrue(Post.objects.filter(author=self.user).exists())

    def test_edit_post(self):
        base_post = self.post.text
        form_data = {
            'author': self.user,
            'text': 'test-text',
            'group': self.group
        }
        response = self.authorized_client.post(
            reverse('posts:post_detail', kwargs={'post_id': '1'}),
            {'text': 'test-text',
            'group': '1'},
            follow = False
        )
        base_post_new = PostFormTests.post

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(base_post_new, self.post.text)
        self.assertFalse(
            Post.objects.filter(
                text='change-test-text'
            ).exists()
        )
        self.assertTrue(
            Post.objects.filter(
                id=1
            ).exists()
        )