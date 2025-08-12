from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.role == User.ADMIN

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
        return request.user and (request.user.role == User.ADMIN or request.user.role == User.STAFF)
    

class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role == User.ADMIN or request.user.role == User.STAFF)


class IsStuffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.role == User.STAFF



class IsAdminOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.member == request.user or request.user.role == User.ADMIN