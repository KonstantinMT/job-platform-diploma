from django import forms

from .models import Company, Vacancy


class CompanyForm(forms.ModelForm):
    """Форма создания компании работодателя."""

    class Meta:
        model = Company
        fields = (
            'name',
            'description',
            'city',
            'website',
        )


class VacancyForm(forms.ModelForm):
    """Форма создания и редактирования вакансии."""

    class Meta:
        model = Vacancy
        fields = (
            'company',
            'title',
            'description',
            'city',
            'salary_from',
            'salary_to',
            'experience',
            'employment_type',
            'skills',
            'is_active',
        )

        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 6}
            ),
        }

    def __init__(self, *args, employer=None, **kwargs):
        super().__init__(*args, **kwargs)

        if employer is not None:
            self.fields['company'].queryset = Company.objects.filter(
                employer=employer
            )
        else:
            self.fields['company'].queryset = Company.objects.none()

    def clean(self):
        cleaned_data = super().clean()

        salary_from = cleaned_data.get('salary_from')
        salary_to = cleaned_data.get('salary_to')

        if (
            salary_from is not None
            and salary_to is not None
            and salary_from > salary_to
        ):
            raise forms.ValidationError(
                'Зарплата "от" не может быть больше зарплаты "до".'
            )

        return cleaned_data