from rest_framework import serializers

from jobs.models import Vacancy
from resumes.models import Resume

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор отклика на вакансию."""

    candidate = serializers.StringRelatedField(
        read_only=True
    )

    candidate_username = serializers.CharField(
        source='candidate.user.username',
        read_only=True
    )

    vacancy_title = serializers.CharField(
        source='vacancy.title',
        read_only=True
    )

    company_name = serializers.CharField(
        source='vacancy.company.name',
        read_only=True
    )

    resume_title = serializers.CharField(
        source='resume.title',
        read_only=True
    )

    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    vacancy = serializers.PrimaryKeyRelatedField(
        queryset=Vacancy.objects.filter(
            is_active=True
        )
    )

    resume = serializers.PrimaryKeyRelatedField(
        queryset=Resume.objects.all()
    )

    class Meta:
        model = Application

        fields = (
            'id',
            'candidate',
            'candidate_username',
            'vacancy',
            'vacancy_title',
            'company_name',
            'resume',
            'resume_title',
            'cover_letter',
            'status',
            'status_display',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'id',
            'candidate',
            'status',
            'created_at',
            'updated_at',
        )

    def validate(self, attrs):
        """Проверяет корректность отклика."""

        request = self.context.get('request')

        if request is None:
            return attrs

        try:
            candidate = request.user.candidate_profile

        except AttributeError:
            raise serializers.ValidationError(
                'Профиль соискателя не найден.'
            )

        vacancy = attrs.get('vacancy')
        resume = attrs.get('resume')

        if resume.candidate_id != candidate.id:
            raise serializers.ValidationError(
                {
                    'resume': (
                        'Можно использовать только '
                        'собственное резюме.'
                    )
                }
            )

        if not resume.is_active:
            raise serializers.ValidationError(
                {
                    'resume': (
                        'Для отклика необходимо '
                        'активное резюме.'
                    )
                }
            )

        if Application.objects.filter(
            candidate=candidate,
            vacancy=vacancy,
        ).exists():
            raise serializers.ValidationError(
                'Вы уже откликались на эту вакансию.'
            )

        return attrs


class ApplicationStatusSerializer(serializers.ModelSerializer):
    """Изменение статуса отклика работодателем."""

    class Meta:
        model = Application

        fields = (
            'status',
        )