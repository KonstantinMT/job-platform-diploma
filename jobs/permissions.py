from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
)


class IsCompanyOwnerOrReadOnly(BasePermission):
    """
    Читать компании могут все.

    Изменять компанию может только
    работодатель-владелец.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.role == 'employer'
        )

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):
        if request.method in SAFE_METHODS:
            return True

        return obj.employer.user_id == request.user.id


class IsVacancyOwnerOrReadOnly(BasePermission):
    """
    Читать вакансии могут все.

    Изменять вакансию может только
    работодатель-владелец.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.role == 'employer'
        )

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):
        if request.method in SAFE_METHODS:
            return True

        return (
            obj.company.employer.user_id
            == request.user.id
        )