from rest_framework import permissions


class IsServiceAccountOrAdmin(permissions.BasePermission):
    """
    Allows access only to staff users or service accounts.
    """

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and (
                user.is_staff
                or getattr(user, "is_service_account", False)
            )
        )