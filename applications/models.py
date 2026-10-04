from django.core.exceptions import ValidationError
from django.db import models


class Application(models.Model):
    """Отклик соискателя на вакансию."""

    class Status(models.TextChoices):
        NEW = 'new', 'Новый'
        REVIEW = 'review', 'На рассмотрении'
        INTERVIEW = 'interview', 'Приглашён на собеседование'
        REJECTED = 'rejected', 'Отклонён'
        ACCEPTED = 'accepted', 'Принят'

    candidate = models.ForeignKey(
        'accounts.CandidateProfile',
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Соискатель'
    )

    vacancy = models.ForeignKey(
        'jobs.Vacancy',
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Вакансия'
    )

    resume = models.ForeignKey(
        'resumes.Resume',
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Резюме'
    )

    cover_letter = models.TextField(
        blank=True,
        verbose_name='Сопроводительное письмо'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name='Статус'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отклика'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['candidate', 'vacancy'],
                name='unique_candidate_vacancy_application'
            )
        ]

    def clean(self):
        """Проверяет, что выбранное резюме принадлежит этому соискателю."""
        if self.resume_id and self.candidate_id:
            if self.resume.candidate_id != self.candidate_id:
                raise ValidationError(
                    'Выбранное резюме не принадлежит этому соискателю.'
                )

    def __str__(self):
        return f'{self.candidate.user.username} → {self.vacancy.title}'