from rest_framework import permissions
from .enums import RoleChoices

class IsAdminOrManagerAddDeveloper(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.role == RoleChoices.ADMIN:
            return True
        elif user.role == RoleChoices.MANAGER:
            return True
        return False
    
class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [RoleChoices.ADMIN, RoleChoices.MANAGER]
