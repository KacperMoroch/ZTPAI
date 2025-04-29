from rest_framework.permissions import BasePermission

class IsAdminUserCustom(BasePermission):
    """
    Umożliwia dostęp tylko użytkownikom będącym superuserami.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
