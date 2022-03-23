from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': 'Текст поста',
            'group': 'Группа'
        }
        help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу'
        }
