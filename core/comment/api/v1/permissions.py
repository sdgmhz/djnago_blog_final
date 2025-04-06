from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ check to see if the author of the comment is implementing with it """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.email == request.user.email
    

class IsVerifiedOrReadOnly(permissions.BasePermission):
    """
    Full access is granted only to verified users.Unverified users are allowed read-only access.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write actions only for authenticated and verified users
        return request.user.is_authenticated and getattr(request.user, 'is_verified', False)
    