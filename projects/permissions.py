from rest_framework.permissions import BasePermission
from accounts.models import User

class IsProjectOwnerOrAdmin(BasePermission):
    """
    Only project owner or admin can modify project
    """

    def has_object_permission(self, request, view, obj):
        return (request.user.role == User.ROLE_ADMIN or obj.owner == request.user)


class CanCreateProject(BasePermission):
    """
    Only admin or manager can create projects
    """

    def has_permission(self, request, view):
        return request.user.role in [User.ROLE_ADMIN, User.ROLE_MANAGER]
