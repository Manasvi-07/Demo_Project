from rest_framework import permissions
from account.enums import RoleChoices

class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [RoleChoices.ADMIN, RoleChoices.MANAGER]
    
class IsAdminManagerOrTaskOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == RoleChoices.ADMIN:
            return True
        if user.role == RoleChoices.MANAGER:
            return hasattr(obj, "project") and obj.project.owner == user
        if user.role == RoleChoices.DEVELOPER:
            return obj.assigned == user
        return False