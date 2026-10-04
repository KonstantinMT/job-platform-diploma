from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import RegistrationForm
from .models import CandidateProfile, EmployerProfile, User


@transaction.atomic
def register(request):
    """Регистрация нового пользователя и создание профиля по его роли."""

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            if user.role == User.Role.CANDIDATE:
                CandidateProfile.objects.create(user=user)

            elif user.role == User.Role.EMPLOYER:
                EmployerProfile.objects.create(user=user)

            login(request, user)

            return redirect('home')

    else:
        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )