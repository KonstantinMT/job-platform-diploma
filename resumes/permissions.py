from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
)


class IsResumeOwnerOrReadOnly(BasePermission):
    """
    Читать активные резюме могут авторизованные пользователи.

    Создавать и изменять резюме может только
    соискатель-владелец.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        return (
            request.user.is_authenticated
            and request.user.role == 'candidate'
        )

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        return (
            obj.candidate.user_id
            == request.user.id
        )