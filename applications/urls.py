from django.urls import path

from . import views


urlpatterns = [
    path(
        'apply/<int:vacancy_id>/',
        views.application_create,
        name='application_create'
    ),

    path(
        'employer/',
        views.employer_applications,
        name='employer_applications'
    ),

    path(
        '<int:pk>/status/',
        views.application_status_update,
        name='application_status_update'
    ),
]