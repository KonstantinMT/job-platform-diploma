from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    """Форма отклика соискателя на вакансию."""

    class Meta:
        model = Application
        fields = (
            'resume',
            'cover_letter',
        )

        widgets = {
            'cover_letter': forms.Textarea(
                attrs={'rows': 5}
            ),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, **kwargs)

        if candidate is not None:
            self.fields['resume'].queryset = candidate.resumes.filter(
                is_active=True
            )
        else:
            self.fields['resume'].queryset = self.fields[
                'resume'
            ].queryset.none()


class ApplicationStatusForm(forms.ModelForm):
    """Форма изменения статуса отклика работодателем."""

    class Meta:
        model = Application
        fields = (
            'status',
        )