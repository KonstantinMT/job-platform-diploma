from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Отклики соискателей на вакансии."""

    list_display = (
        'candidate',
        'vacancy',
        'resume',
        'status',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'candidate__user__username',
        'vacancy__title',
        'resume__title',
    )