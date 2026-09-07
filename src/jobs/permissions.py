from rest_framework.permissions import BasePermission
from users.models import UserRole

class IsJobCreatorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == UserRole.ADMIN:
            return True
        return obj.creator_id == request.user.id

class IsJobAssigneeOrCreatorOrManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role in (UserRole.ADMIN, UserRole.MANAGER):
            return True
        return obj.creator_id == request.user.id or obj.assignee_id == request.user.id
