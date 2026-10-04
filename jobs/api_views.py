from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)

from .models import Company, Skill, Vacancy
from .permissions import (
    IsCompanyOwnerOrReadOnly,
    IsVacancyOwnerOrReadOnly,
)
from .serializers import (
    CompanySerializer,
    SkillSerializer,
    VacancySerializer,
)


class CompanyViewSet(ModelViewSet):
    """REST API компаний."""

    serializer_class = CompanySerializer
    permission_classes = (
        IsCompanyOwnerOrReadOnly,
    )

    filterset_fields = (
        'city',
    )

    search_fields = (
        'name',
        'description',
        'city',
    )

    ordering_fields = (
        'name',
        'created_at',
    )

    ordering = (
        'name',
    )

    def get_queryset(self):
        return Company.objects.select_related(
            'employer__user'
        ).all()

    def perform_create(self, serializer):
        try:
            employer = self.request.user.employer_profile

        except AttributeError:
            raise PermissionDenied(
                'Профиль работодателя не найден.'
            )

        serializer.save(
            employer=employer
        )


class SkillViewSet(ReadOnlyModelViewSet):
    """REST API навыков только для чтения."""

    queryset = Skill.objects.all().order_by('name')
    serializer_class = SkillSerializer

    search_fields = (
        'name',
    )


class VacancyViewSet(ModelViewSet):
    """REST API вакансий."""

    serializer_class = VacancySerializer
    permission_classes = (
        IsVacancyOwnerOrReadOnly,
    )

    filterset_fields = (
        'city',
        'experience',
        'employment_type',
        'is_active',
        'company',
    )

    search_fields = (
        'title',
        'description',
        'company__name',
        'city',
    )

    ordering_fields = (
        'created_at',
        'salary_from',
        'salary_to',
        'title',
    )

    ordering = (
        '-created_at',
    )

    def get_queryset(self):
        queryset = Vacancy.objects.select_related(
            'company',
            'company__employer__user',
        ).prefetch_related(
            'skills'
        )

        user = self.request.user

        if (
            user.is_authenticated
            and user.role == 'employer'
        ):
            return queryset.filter(
                Q(is_active=True)
                | Q(company__employer__user=user)
            ).distinct()

        return queryset.filter(
            is_active=True
        )

    def perform_create(self, serializer):
        company = serializer.validated_data['company']

        if (
            company.employer.user_id
            != self.request.user.id
        ):
            raise PermissionDenied(
                'Нельзя создать вакансию '
                'для чужой компании.'
            )

        serializer.save()

    def perform_update(self, serializer):
        company = serializer.validated_data.get(
            'company',
            serializer.instance.company
        )

        if (
            company.employer.user_id
            != self.request.user.id
        ):
            raise PermissionDenied(
                'Нельзя перенести вакансию '
                'в чужую компанию.'
            )

        serializer.save()