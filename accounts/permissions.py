from rest_framework.permissions import BasePermission
from .models import User

class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_ADMIN


class IsManagerOrAdmin(BasePermission):
    """
    Allows access to managers and admins.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [User.ROLE_ADMIN, User.ROLE_MANAGER]
        )


class IsSelfOrAdmin(BasePermission):
    """
    Object-level permission:
    user can access their own profile or admin can access anyone.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.role == User.ROLE_ADMIN or obj == request.user