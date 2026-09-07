from rest_framework.permissions import BasePermission
from users.models import UserRole

class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.ADMIN)

class IsManagerUserRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in (UserRole.MANAGER, UserRole.ADMIN)
        )

class IsMemberUserRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
