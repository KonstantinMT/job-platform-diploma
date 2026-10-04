from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.vacancy_list,
        name='vacancy_list'
    ),

    path(
        '<int:pk>/',
        views.vacancy_detail,
        name='vacancy_detail'
    ),

    path(
        'employer/dashboard/',
        views.employer_dashboard,
        name='employer_dashboard'
    ),

    path(
        'employer/company/create/',
        views.company_create,
        name='company_create'
    ),

    path(
        'employer/create/',
        views.vacancy_create,
        name='vacancy_create'
    ),

    path(
        'employer/<int:pk>/edit/',
        views.vacancy_update,
        name='vacancy_update'
    ),

    path(
        'employer/<int:pk>/delete/',
        views.vacancy_delete,
        name='vacancy_delete'
    ),
]