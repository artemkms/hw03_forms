from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Идентификатор', unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/group/{self.slug}/"

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField('Текст поста', help_text='Текст поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        related_name="group",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Выберите группу'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
