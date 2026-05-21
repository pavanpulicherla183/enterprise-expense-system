"""
Custom role-based permissions.
"""

from rest_framework.permissions import BasePermission

from claims.models.user import UserRole


class IsEmployee(BasePermission):
    """
    Allows access only to employees.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.EMPLOYEE
        )


class IsReviewer(BasePermission):
    """
    Allows access only to reviewers.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.REVIEWER
        )


class IsController(BasePermission):
    """
    Allows access only to finance controllers.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.CONTROLLER
        )