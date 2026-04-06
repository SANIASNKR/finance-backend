from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Only admin users can access this.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


class IsAnalystOrAdmin(BasePermission):
    """
    Only analysts and admins can access this.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['analyst', 'admin']
        )


class IsViewerOrAbove(BasePermission):
    """
    Any logged in user can access this.
    Viewer, Analyst, and Admin all pass.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated
        )