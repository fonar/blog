from rest_framework.permissions import BasePermission


class IsEditor(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and
            user.is_authenticated and
            hasattr(user, 'writer') and
            user.writer.is_editor
        )
