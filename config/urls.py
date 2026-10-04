from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'accounts/',
        include('accounts.urls')
    ),

    path(
        'vacancies/',
        include('jobs.urls')
    ),

    path(
        'resumes/',
        include('resumes.urls')
    ),

    path(
        'applications/',
        include('applications.urls')
    ),

    path(
        'api/',
        include('config.api_urls')
    ),

    path(
        '',
        views.home,
        name='home'
    ),
]