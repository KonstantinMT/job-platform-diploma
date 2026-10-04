from rest_framework import serializers

from .models import Company, Skill, Vacancy


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор профессиональных навыков."""

    class Meta:
        model = Skill
        fields = (
            'id',
            'name',
        )


class CompanySerializer(serializers.ModelSerializer):
    """Сериализатор компании."""

    employer = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Company
        fields = (
            'id',
            'employer',
            'name',
            'description',
            'city',
            'website',
            'created_at',
        )

        read_only_fields = (
            'id',
            'employer',
            'created_at',
        )


class VacancySerializer(serializers.ModelSerializer):
    """Сериализатор вакансии."""

    company_name = serializers.CharField(
        source='company.name',
        read_only=True
    )

    skills = SkillSerializer(
        many=True,
        read_only=True
    )

    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        source='skills',
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Vacancy
        fields = (
            'id',
            'company',
            'company_name',
            'title',
            'description',
            'city',
            'salary_from',
            'salary_to',
            'experience',
            'employment_type',
            'skills',
            'skill_ids',
            'is_active',
            'created_at',
        )

        read_only_fields = (
            'id',
            'created_at',
        )

    def validate(self, attrs):
        """Проверяет диапазон зарплаты."""

        salary_from = attrs.get(
            'salary_from',
            getattr(self.instance, 'salary_from', None)
        )

        salary_to = attrs.get(
            'salary_to',
            getattr(self.instance, 'salary_to', None)
        )

        if (
            salary_from is not None
            and salary_to is not None
            and salary_from > salary_to
        ):
            raise serializers.ValidationError(
                {
                    'salary': (
                        'Зарплата "от" не может быть '
                        'больше зарплаты "до".'
                    )
                }
            )

        return attrs