from rest_framework.permissions import BasePermission

class IsSubscriptionOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.member == request.user