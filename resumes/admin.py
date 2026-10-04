from django.contrib import admin

from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """Резюме соискателей."""

    list_display = (
        'title',
        'candidate',
        'city',
        'desired_salary',
        'is_active',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'is_active',
        'city',
    )

    search_fields = (
        'title',
        'candidate__user__username',
        'city',
        'summary',
    )

    filter_horizontal = (
        'skills',
    )