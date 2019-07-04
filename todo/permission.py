from rest_framework import permissions


class IsOrganizationUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.organization == request.user.profilemodel.active_organization

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
