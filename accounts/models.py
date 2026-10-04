from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь платформы."""

    class Role(models.TextChoices):
        CANDIDATE = 'candidate', 'Соискатель'
        EMPLOYER = 'employer', 'Работодатель'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        blank=True,
        verbose_name='Роль пользователя'
    )

    def __str__(self):
        return self.username


class CandidateProfile(models.Model):
    """Профиль пользователя с ролью соискателя."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='candidate_profile',
        verbose_name='Пользователь'
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Город'
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Телефон'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'Профиль соискателя: {self.user.username}'


class EmployerProfile(models.Model):
    """Профиль пользователя с ролью работодателя."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employer_profile',
        verbose_name='Пользователь'
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Телефон'
    )

    position = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Должность'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'Профиль работодателя: {self.user.username}'