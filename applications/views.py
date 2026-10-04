from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import (
    CandidateProfile,
    EmployerProfile,
    User,
)
from jobs.models import Vacancy

from .forms import ApplicationForm, ApplicationStatusForm
from .models import Application


def get_candidate_profile(user):
    """Возвращает профиль соискателя или запрещает доступ."""

    if user.role != User.Role.CANDIDATE:
        raise PermissionDenied(
            'Откликаться на вакансии могут только соискатели.'
        )

    try:
        return user.candidate_profile

    except CandidateProfile.DoesNotExist:
        raise PermissionDenied(
            'Профиль соискателя не найден.'
        )


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


@login_required
def application_create(request, vacancy_id):
    """Создание отклика на вакансию."""

    candidate = get_candidate_profile(request.user)

    vacancy = get_object_or_404(
        Vacancy,
        pk=vacancy_id,
        is_active=True,
    )

    already_applied = Application.objects.filter(
        candidate=candidate,
        vacancy=vacancy,
    ).exists()

    if already_applied:
        messages.warning(
            request,
            'Вы уже откликались на эту вакансию.'
        )

        return redirect(
            'vacancy_detail',
            pk=vacancy.pk,
        )

    if request.method == 'POST':
        form = ApplicationForm(
            request.POST,
            candidate=candidate,
        )

        if form.is_valid():
            application = form.save(commit=False)

            application.candidate = candidate
            application.vacancy = vacancy

            application.full_clean()
            application.save()

            messages.success(
                request,
                'Отклик успешно отправлен.'
            )

            return redirect('candidate_dashboard')

    else:
        form = ApplicationForm(
            candidate=candidate
        )

    return render(
        request,
        'applications/application_form.html',
        {
            'form': form,
            'vacancy': vacancy,
        }
    )


@login_required
def employer_applications(request):
    """Все отклики на вакансии текущего работодателя."""

    employer = get_employer_profile(request.user)

    applications = Application.objects.filter(
        vacancy__company__employer=employer
    ).select_related(
        'candidate__user',
        'vacancy',
        'vacancy__company',
        'resume',
    ).order_by('-created_at')

    return render(
        request,
        'applications/employer_applications.html',
        {
            'applications': applications,
        }
    )


@login_required
def application_status_update(request, pk):
    """Изменение статуса отклика владельцем вакансии."""

    employer = get_employer_profile(request.user)

    application = get_object_or_404(
        Application,
        pk=pk,
        vacancy__company__employer=employer,
    )

    if request.method == 'POST':
        form = ApplicationStatusForm(
            request.POST,
            instance=application,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Статус отклика изменён.'
            )

            return redirect('employer_applications')

    else:
        form = ApplicationStatusForm(
            instance=application
        )

    return render(
        request,
        'applications/application_status_form.html',
        {
            'form': form,
            'application': application,
        }
    )