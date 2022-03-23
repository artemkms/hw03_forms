from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm

User = get_user_model()


#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm
class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # укажем модель, с которой связана создаваемая форма
        model = get_user_model()
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('first_name', 'last_name', 'username', 'email')


class PasswordChange(PasswordChangeForm):
    form = PasswordChangeForm

    class Meta:
        model = get_user_model()
        fields = (
            'old_password',
            'new_password1',
            'new_password2',
        )
