from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # check permissions for read-only request
            return True
        else:
            # check permissions for write request
            return bool(request.user and request.user.is_staff)


class ReviewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # check permissions for read-only request
            return True
        else:
            # check permissions for write request
            return obj.created_by == request.user