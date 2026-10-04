from django.db import models


class Resume(models.Model):
    """Резюме соискателя."""

    candidate = models.ForeignKey(
        'accounts.CandidateProfile',
        on_delete=models.CASCADE,
        related_name='resumes',
        verbose_name='Соискатель'
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Желаемая должность'
    )

    summary = models.TextField(
        blank=True,
        verbose_name='О себе'
    )

    experience = models.TextField(
        blank=True,
        verbose_name='Опыт работы'
    )

    education = models.TextField(
        blank=True,
        verbose_name='Образование'
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Город'
    )

    desired_salary = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Желаемая зарплата'
    )

    skills = models.ManyToManyField(
        'jobs.Skill',
        blank=True,
        related_name='resumes',
        verbose_name='Навыки'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    def __str__(self):
        return self.title