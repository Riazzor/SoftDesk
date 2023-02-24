from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Can edit if is owner. Else read only.
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD or OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author_user == request.user:
            return True

        return False
