from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User

class IsAdminOrStaffReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            if request.user  and (request.user.role == User.ADMIN or request.user.role == User.STAFF):
                return True
            return False    
        return request.user and request.user.role == User.ADMIN 
    