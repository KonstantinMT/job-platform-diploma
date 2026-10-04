from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import EmployerProfile, User

from .forms import CompanyForm, VacancyForm
from .models import Vacancy


def get_employer_profile(user):
    """Возвращает профиль работодателя или запрещает доступ."""

    if user.role != User.Role.EMPLOYER:
        raise PermissionDenied(
            'Эта страница доступна только работодателям.'
        )

    try:
        return user.employer_profile

    except EmployerProfile.DoesNotExist:
        raise PermissionDenied(
            'Профиль работодателя не найден.'
        )


def vacancy_list(request):
    """Список активных вакансий с поиском, фильтрацией и сортировкой."""

    vacancies = Vacancy.objects.filter(
        is_active=True
    ).select_related('company').prefetch_related('skills')

    query = request.GET.get('q', '').strip()

    if query:
        vacancies = vacancies.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(company__name__icontains=query)
        )

    city = request.GET.get('city', '').strip()

    if city:
        vacancies = vacancies.filter(
            city__icontains=city
        )

    employment_type = request.GET.get(
        'employment_type',
        ''
    )

    if employment_type:
        vacancies = vacancies.filter(
            employment_type=employment_type
        )

    experience = request.GET.get(
        'experience',
        ''
    )

    if experience:
        vacancies = vacancies.filter(
            experience=experience
        )

    salary_min = request.GET.get(
        'salary_min',
        ''
    )

    if salary_min.isdigit():
        vacancies = vacancies.filter(
            salary_to__gte=int(salary_min)
        )

    ordering = request.GET.get(
        'ordering',
        '-created_at'
    )

    allowed_ordering = {
        '-created_at',
        'created_at',
        'salary_from',
        '-salary_from',
        'title',
    }

    if ordering not in allowed_ordering:
        ordering = '-created_at'

    vacancies = vacancies.order_by(ordering)

    paginator = Paginator(vacancies, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'employment_types': Vacancy.EmploymentType.choices,
        'experience_levels': Vacancy.ExperienceLevel.choices,
    }

    return render(
        request,
        'jobs/vacancy_list.html',
        context
    )


def vacancy_detail(request, pk):
    """Подробная страница одной активной вакансии."""

    vacancy = get_object_or_404(
        Vacancy.objects.select_related(
            'company'
        ).prefetch_related('skills'),
        pk=pk,
        is_active=True,
    )

    return render(
        request,
        'jobs/vacancy_detail.html',
        {'vacancy': vacancy}
    )


@login_required
def employer_dashboard(request):
    """Личный кабинет работодателя."""

    employer = get_employer_profile(request.user)

    companies = employer.companies.all()

    vacancies = Vacancy.objects.filter(
        company__employer=employer
    ).select_related('company').order_by('-created_at')

    context = {
        'companies': companies,
        'vacancies': vacancies,
    }

    return render(
        request,
        'jobs/employer_dashboard.html',
        context
    )


@login_required
def company_create(request):
    """Создание компании текущего работодателя."""

    employer = get_employer_profile(request.user)

    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():
            company = form.save(commit=False)
            company.employer = employer
            company.save()

            return redirect('employer_dashboard')

    else:
        form = CompanyForm()

    return render(
        request,
        'jobs/company_form.html',
        {'form': form}
    )


@login_required
def vacancy_create(request):
    """Создание вакансии работодателем."""

    employer = get_employer_profile(request.user)

    if request.method == 'POST':
        form = VacancyForm(
            request.POST,
            employer=employer
        )

        if form.is_valid():
            form.save()

            return redirect('employer_dashboard')

    else:
        form = VacancyForm(
            employer=employer
        )

    return render(
        request,
        'jobs/vacancy_form.html',
        {
            'form': form,
            'page_title': 'Создание вакансии',
        }
    )


@login_required
def vacancy_update(request, pk):
    """Редактирование только собственной вакансии."""

    employer = get_employer_profile(request.user)

    vacancy = get_object_or_404(
        Vacancy,
        pk=pk,
        company__employer=employer,
    )

    if request.method == 'POST':
        form = VacancyForm(
            request.POST,
            instance=vacancy,
            employer=employer,
        )

        if form.is_valid():
            form.save()

            return redirect('employer_dashboard')

    else:
        form = VacancyForm(
            instance=vacancy,
            employer=employer,
        )

    return render(
        request,
        'jobs/vacancy_form.html',
        {
            'form': form,
            'page_title': 'Редактирование вакансии',
        }
    )


@login_required
def vacancy_delete(request, pk):
    """Удаление только собственной вакансии."""

    employer = get_employer_profile(request.user)

    vacancy = get_object_or_404(
        Vacancy,
        pk=pk,
        company__employer=employer,
    )

    if request.method == 'POST':
        vacancy.delete()

        return redirect('employer_dashboard')

    return render(
        request,
        'jobs/vacancy_confirm_delete.html',
        {'vacancy': vacancy}
    )