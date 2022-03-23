from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm

# Create your views here.


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class ChangePassword(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
