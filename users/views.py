from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import User
from .serializers import  UserSerializer
from .permissions import IsAdminOrStaffReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from core.serializers import SwaggerErrorResponseSerializer

# class ProfileImageViewSet(ModelViewSet):
#     serializer_class = ProfileImageSerializer
#     permission_classes = [IsUserSelfOrAdmin]

#     def get_queryset(self):
#         return ProfileImage.objects.filter(user_id=self.kwargs.get('user_pk'))

#     def perform_create(self, serializer):
#         serializer.save(user_id=self.kwargs.get('user_pk'))

class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrStaffReadOnly]

    @swagger_auto_schema(
        operation_summary="Create User",
        operation_description="Create User. Admin can create for any member, Staff/Member can not create for user.",
        responses={
            201: UserSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="List Users",
        operation_description="List Users. Admin/Staff can list for any member.",
        responses={
            200: UserSerializer(many=True),
            401: SwaggerErrorResponseSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Retrieve User",
        operation_description="Retrieve User. Admin/Staff can retrieve for any member, Member can retrieve for themselves.",
        responses={
            200: UserSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update User",
        operation_description="Update User. Admin update for any member. Staff/Member can update for themselves.",
        responses={
            200: UserSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Partial Update User",
        operation_description="Partial Update User. Admin update for any member, Staff/Member can not update for user. Member can update for themselves.",
        responses={
            200: UserSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete User",
        operation_description="Delete User. Admin delete for any member, Staff/Member can not delete for user.",
        responses={
            204: openapi.Response(description="No Content"),
            401: SwaggerErrorResponseSerializer,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)