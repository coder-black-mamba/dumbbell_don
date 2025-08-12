from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User

class IsAdminOrSelfOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and (request.user.role == User.ADMIN or request.user.role == User.MEMBER) 