from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from .models import Resume
from .permissions import IsResumeOwnerOrReadOnly
from .serializers import ResumeSerializer


class ResumeViewSet(ModelViewSet):
    """REST API резюме."""

    serializer_class = ResumeSerializer

    permission_classes = (
        IsResumeOwnerOrReadOnly,
    )

    filterset_fields = (
        'city',
        'is_active',
        'skills',
    )

    search_fields = (
        'title',
        'summary',
        'experience',
        'education',
        'city',
        'skills__name',
    )

    ordering_fields = (
        'created_at',
        'updated_at',
        'desired_salary',
        'title',
    )

    ordering = (
        '-updated_at',
    )

    def get_queryset(self):
        queryset = Resume.objects.select_related(
            'candidate__user'
        ).prefetch_related(
            'skills'
        )

        user = self.request.user

        if not user.is_authenticated:
            return queryset.none()

        if user.role == 'candidate':
            return queryset.filter(
                candidate__user=user
            )

        if user.role == 'employer':
            return queryset.filter(
                is_active=True
            )

        return queryset.none()

    def perform_create(self, serializer):
        try:
            candidate = self.request.user.candidate_profile

        except AttributeError:
            raise PermissionDenied(
                'Профиль соискателя не найден.'
            )

        serializer.save(
            candidate=candidate
        )