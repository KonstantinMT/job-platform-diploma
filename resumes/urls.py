from django.urls import path

from . import views


urlpatterns = [
    path(
        'dashboard/',
        views.candidate_dashboard,
        name='candidate_dashboard'
    ),

    path(
        'create/',
        views.resume_create,
        name='resume_create'
    ),

    path(
        '<int:pk>/edit/',
        views.resume_update,
        name='resume_update'
    ),

    path(
        '<int:pk>/delete/',
        views.resume_delete,
        name='resume_delete'
    ),
]