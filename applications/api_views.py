from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Application
from .serializers import (
    ApplicationSerializer,
    ApplicationStatusSerializer,
)


class ApplicationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    """REST API откликов."""

    serializer_class = ApplicationSerializer

    permission_classes = (
        IsAuthenticated,
    )

    def get_queryset(self):
        """Возвращает отклики в зависимости от роли пользователя."""

        queryset = Application.objects.select_related(
            'candidate__user',
            'vacancy',
            'vacancy__company',
            'vacancy__company__employer__user',
            'resume',
        ).order_by('-created_at')

        user = self.request.user

        if user.role == 'candidate':
            return queryset.filter(
                candidate__user=user
            )

        if user.role == 'employer':
            return queryset.filter(
                vacancy__company__employer__user=user
            )

        return queryset.none()

    def perform_create(self, serializer):
        """Создаёт отклик от имени текущего соискателя."""

        user = self.request.user

        if user.role != 'candidate':
            raise PermissionDenied(
                'Создавать отклики могут только соискатели.'
            )

        try:
            candidate = user.candidate_profile

        except AttributeError:
            raise PermissionDenied(
                'Профиль соискателя не найден.'
            )

        serializer.save(
            candidate=candidate
        )

    @extend_schema(
        request=ApplicationStatusSerializer,
        responses={
            200: ApplicationSerializer,
        },
        description='Работодатель изменяет статус отклика.'
    )
    @action(
        detail=True,
        methods=['patch'],
        url_path='status',
    )
    def change_status(self, request, pk=None):
        """Работодатель изменяет статус отклика."""

        if request.user.role != 'employer':
            raise PermissionDenied(
                'Изменять статус может только работодатель.'
            )

        application = self.get_object()

        serializer = ApplicationStatusSerializer(
            application,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        response_serializer = ApplicationSerializer(
            application,
            context={
                'request': request,
            }
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )