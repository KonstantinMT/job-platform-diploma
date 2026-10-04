from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import CandidateProfile, User

from .forms import ResumeForm
from .models import Resume


def get_candidate_profile(user):
    """Возвращает профиль соискателя или запрещает доступ."""

    if user.role != User.Role.CANDIDATE:
        raise PermissionDenied(
            'Эта страница доступна только соискателям.'
        )

    try:
        return user.candidate_profile

    except CandidateProfile.DoesNotExist:
        raise PermissionDenied(
            'Профиль соискателя не найден.'
        )


@login_required
def candidate_dashboard(request):
    """Личный кабинет соискателя."""

    candidate = get_candidate_profile(request.user)

    resumes = candidate.resumes.all().order_by(
        '-updated_at'
    )

    applications = candidate.applications.select_related(
        'vacancy',
        'vacancy__company',
        'resume',
    ).order_by('-created_at')

    context = {
        'candidate': candidate,
        'resumes': resumes,
        'applications': applications,
    }

    return render(
        request,
        'resumes/candidate_dashboard.html',
        context
    )


@login_required
def resume_create(request):
    """Создание резюме текущим соискателем."""

    candidate = get_candidate_profile(request.user)

    if request.method == 'POST':
        form = ResumeForm(request.POST)

        if form.is_valid():
            resume = form.save(commit=False)

            resume.candidate = candidate

            resume.save()

            form.save_m2m()

            return redirect('candidate_dashboard')

    else:
        form = ResumeForm()

    return render(
        request,
        'resumes/resume_form.html',
        {
            'form': form,
            'page_title': 'Создание резюме',
        }
    )


@login_required
def resume_update(request, pk):
    """Редактирование только собственного резюме."""

    candidate = get_candidate_profile(request.user)

    resume = get_object_or_404(
        Resume,
        pk=pk,
        candidate=candidate,
    )

    if request.method == 'POST':
        form = ResumeForm(
            request.POST,
            instance=resume,
        )

        if form.is_valid():
            form.save()

            return redirect('candidate_dashboard')

    else:
        form = ResumeForm(
            instance=resume
        )

    return render(
        request,
        'resumes/resume_form.html',
        {
            'form': form,
            'page_title': 'Редактирование резюме',
        }
    )


@login_required
def resume_delete(request, pk):
    """Удаление только собственного резюме."""

    candidate = get_candidate_profile(request.user)

    resume = get_object_or_404(
        Resume,
        pk=pk,
        candidate=candidate,
    )

    if request.method == 'POST':
        resume.delete()

        return redirect('candidate_dashboard')

    return render(
        request,
        'resumes/resume_confirm_delete.html',
        {'resume': resume}
    )