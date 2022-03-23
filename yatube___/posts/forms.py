from django import forms
from django.core.validators import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')

    def clean_text(self):
        text = self.cleaned_data['text']
        if text == '':
            raise ValidationError('Введите текст!')
        return text
