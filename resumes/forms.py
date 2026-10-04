from django import forms

from .models import Resume


class ResumeForm(forms.ModelForm):
    """Форма создания и редактирования резюме."""

    class Meta:
        model = Resume
        fields = (
            'title',
            'summary',
            'experience',
            'education',
            'city',
            'desired_salary',
            'skills',
            'is_active',
        )

        widgets = {
            'summary': forms.Textarea(
                attrs={'rows': 5}
            ),
            'experience': forms.Textarea(
                attrs={'rows': 5}
            ),
            'education': forms.Textarea(
                attrs={'rows': 4}
            ),
        }