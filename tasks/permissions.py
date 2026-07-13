from rest_framework.permissions import BasePermission
from accounts.models import User

class IsTaskOwnerAssigneeOrAdmin(BasePermission):
    """
    Admin OR task creator OR assignee
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == User.ROLE_ADMIN
            or obj.created_by == request.user
            or obj.assignee == request.user
        )


class CanCreateTask(BasePermission):
    """
    Only admin or manager can create tasks
    """

    def has_permission(self, request, view):
        return request.user.role in [User.ROLE_ADMIN, User.ROLE_MANAGER]