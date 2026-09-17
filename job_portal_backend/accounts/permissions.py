from rest_framework.permissions import BasePermission
from .models import UserRole

class IsCandidate(BasePermission):
    message = "Only candidates can access this resource."
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.CANDIDATE
        )

class IsRecruiter(BasePermission):
    message = "Only recruiters can access this resource."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.RECRUITER
        )

class IsAdmin(BasePermission):
    message = "Only admins can access this resource."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )

class IsNotBlocked(BasePermission):
    message = "Your account has been blocked."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and not request.user.is_blocked
        )    