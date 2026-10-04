from django.db import models


class Company(models.Model):
    """Компания, принадлежащая работодателю."""

    employer = models.ForeignKey(
        'accounts.EmployerProfile',
        on_delete=models.CASCADE,
        related_name='companies',
        verbose_name='Работодатель'
    )

    name = models.CharField(
        max_length=150,
        verbose_name='Название компании'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание компании'
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Город'
    )

    website = models.URLField(
        blank=True,
        verbose_name='Сайт'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Skill(models.Model):
    """Профессиональный навык."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Навык'
    )

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    """Вакансия компании."""

    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Полная занятость'
        PART_TIME = 'part_time', 'Частичная занятость'
        CONTRACT = 'contract', 'Контракт'
        INTERNSHIP = 'internship', 'Стажировка'

    class ExperienceLevel(models.TextChoices):
        NO_EXPERIENCE = 'no_experience', 'Без опыта'
        ONE_TO_THREE = '1_3', 'От 1 до 3 лет'
        THREE_TO_SIX = '3_6', 'От 3 до 6 лет'
        SIX_PLUS = '6_plus', 'Более 6 лет'

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='Компания'
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Название вакансии'
    )

    description = models.TextField(
        verbose_name='Описание вакансии'
    )

    city = models.CharField(
        max_length=100,
        verbose_name='Город'
    )

    salary_from = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Зарплата от'
    )

    salary_to = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Зарплата до'
    )

    experience = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.NO_EXPERIENCE,
        verbose_name='Опыт работы'
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME,
        verbose_name='Тип занятости'
    )

    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name='vacancies',
        verbose_name='Навыки'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'

    def __str__(self):
        return self.title