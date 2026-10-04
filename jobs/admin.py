from django.contrib import admin

from .models import Company, Skill, Vacancy


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Компании работодателей."""

    list_display = (
        'name',
        'employer',
        'city',
        'website',
        'created_at',
    )

    search_fields = (
        'name',
        'city',
        'employer__user__username',
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Профессиональные навыки."""

    list_display = (
        'name',
    )

    search_fields = (
        'name',
    )


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """Вакансии компаний."""

    list_display = (
        'title',
        'company',
        'city',
        'salary_from',
        'salary_to',
        'employment_type',
        'is_active',
        'created_at',
    )

    list_filter = (
        'employment_type',
        'experience',
        'is_active',
    )

    search_fields = (
        'title',
        'company__name',
        'city',
        'description',
    )

    filter_horizontal = (
        'skills',
    )