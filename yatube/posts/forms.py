from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group',)
        labels = {'verbose_name': 'Название компании'}
