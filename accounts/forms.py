from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    """Форма регистрации пользователя на платформе."""

    role = forms.ChoiceField(
        choices=User.Role.choices,
        required=True,
        label='Роль'
    )

    email = forms.EmailField(
        required=True,
        label='Электронная почта'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'password1',
            'password2',
        )