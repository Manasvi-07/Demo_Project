from rest_framework.permissions import BasePermission
from .enums import RoleChoices

class BaseRolePermission(BasePermission):
    allowed_roles: tuple = ()

    def has_permission(self, request, view):
        user = request.user
        return (
            user
            and user.is_authenticated
            and user.role in self.allowed_roles
        )

class IsAdminOrManager(BaseRolePermission):
    allowed_roles = (RoleChoices.ADMIN, RoleChoices.MANAGER)