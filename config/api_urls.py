from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from applications.api_views import ApplicationViewSet
from jobs.api_views import (
    CompanyViewSet,
    SkillViewSet,
    VacancyViewSet,
)
from resumes.api_views import ResumeViewSet


router = DefaultRouter()

router.register(
    'companies',
    CompanyViewSet,
    basename='api-company'
)

router.register(
    'skills',
    SkillViewSet,
    basename='api-skill'
)

router.register(
    'vacancies',
    VacancyViewSet,
    basename='api-vacancy'
)

router.register(
    'resumes',
    ResumeViewSet,
    basename='api-resume'
)

router.register(
    'applications',
    ApplicationViewSet,
    basename='api-application'
)


urlpatterns = [
    path(
        '',
        include(router.urls)
    ),

    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    path(
        'schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),

    path(
        'docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='swagger-ui'
    ),
]