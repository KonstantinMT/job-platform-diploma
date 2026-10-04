from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CandidateProfile, EmployerProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Настройка отображения нашей модели User в Django Admin."""

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            'Роль на платформе',
            {
                'fields': ('role',),
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            'Роль на платформе',
            {
                'fields': ('role',),
            },
        ),
    )

    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    """Профили соискателей."""

    list_display = (
        'user',
        'city',
        'phone',
        'created_at',
    )

    search_fields = (
        'user__username',
        'city',
        'phone',
    )


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    """Профили работодателей."""

    list_display = (
        'user',
        'position',
        'phone',
        'created_at',
    )

    search_fields = (
        'user__username',
        'position',
        'phone',
    )