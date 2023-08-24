from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )


class IsAdminOrIfAuthenticatedReadCreateDeleteOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.user and request.user.is_staff)
            or (request.method in SAFE_METHODS + ("POST", "DELETE")
                and request.user
                and request.user.is_authenticated
                and not request.user.is_staff)
        )
