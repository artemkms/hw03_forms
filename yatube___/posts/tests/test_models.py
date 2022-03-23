from django.test import TestCase

from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост потому что здесь слишком короткий текст',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        group = PostModelTest.group
        post_str = post.text[:15]
        group_str = group.title
        self.assertEqual(post_str, post.__str__(),
                         'Метод __str__ у объета Post работает неправильно')
        self.assertEqual(group_str, group.__str__(),
                         'Метод __str__ у объекта Group работает неправльно')
