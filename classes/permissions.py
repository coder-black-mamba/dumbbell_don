from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User

class IsStaffOrAdminAndReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and( (request.user.is_staff and request.user.role == User.ADMIN) or (request.user.role == User.STAFF))



class IsStuffOrSelfOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and (request.user.role == User.ADMIN or request.user.role == User.STAFF)    
    
    def has_object_permission(self, request, view, obj): 
        if request.method in SAFE_METHODS:
            return obj.booking.member == request.user
        return request.user.role == User.ADMIN or request.user.role == User.STAFF



class BookingPermission(BasePermission): 
    def has_object_permission(self, request, view, obj):
        if request.user.role == User.ADMIN:
            return True
        if request.method in SAFE_METHODS:
            return obj.member == request.user
        return False