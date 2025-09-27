from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return request.user.role in [User.ADMIN]
        return False

class IsUserSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsUserSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.role == User.ADMIN


class IsStaffOrAdminAndReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return request.user.role in [User.ADMIN, User.STAFF]
        return False
    

class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role in [User.ADMIN, User.STAFF]
        return False


class IsStuffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return request.user.role in [User.ADMIN, User.STAFF]
        return False



class IsAdminOrSelf(BasePermission):
    def has_permission(self, request, view):
        # Allow all authenticated users to access the view
        # Object-level permissions will be checked in has_object_permission
        return request.user and request.user.is_authenticated
        
    def has_object_permission(self, request, view, obj):
        # Allow if user is admin or the owner of the object
        return obj.member == request.user or request.user.role == User.ADMIN