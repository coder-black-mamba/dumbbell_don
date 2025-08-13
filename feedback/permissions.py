from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User

class IsAdminOrSelfOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == User.ADMIN:
            return True
        if request.method in SAFE_METHODS:
            return True
        return request.user==obj.member
    
   