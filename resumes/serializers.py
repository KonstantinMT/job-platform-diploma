from rest_framework import serializers

from jobs.models import Skill
from jobs.serializers import SkillSerializer

from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    """Сериализатор резюме соискателя."""

    candidate = serializers.StringRelatedField(
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
        model = Resume

        fields = (
            'id',
            'candidate',
            'title',
            'summary',
            'experience',
            'education',
            'city',
            'desired_salary',
            'skills',
            'skill_ids',
            'is_active',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'id',
            'candidate',
            'created_at',
            'updated_at',
        )