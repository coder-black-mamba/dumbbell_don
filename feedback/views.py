from .models import Feedback
from .serializers import FeedbackSerializer
from core.utils.BASEModelViewSet import BaseModelViewSet
from .permissions import IsAdminOrSelfOrReadOnly
from users.models import User
from core.utils.api_response import success_response
from core.serializers import SwaggerErrorResponseSerializer

from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
class FeedbackViewSet(BaseModelViewSet):
    # queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOrSelfOrReadOnly]

    # core busineses logic
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN:
            return Feedback.objects.all()
        if self.request.user.role == User.STAFF:
            return Feedback.objects.filter(fitness_class__instructor=self.request.user)
        return Feedback.objects.filter()
    
    # def get_object(self):
    #     if self.request.user.role == User.ADMIN:
    #         return super().get_object()
    #     return Feedback.objects.get(member=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(member=self.request.user) 

    #  Swagger Documentation
    @swagger_auto_schema(
        operation_summary="Create Feedback",
        operation_description="Create Feedback. Admin/Staff sees all, Member sees their own.",
        responses={
            201: FeedbackSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Retrieve feedback record (Admin/Staff sees all)",
        operation_description="Retrieve feedback record (Admin/Staff sees all) Member Can See His Feedback",
        responses={
            200: FeedbackSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
        
    @swagger_auto_schema(
        operation_summary="List feedback records (Admin/Staff sees all)",
        operation_description="List feedback records (Admin/Staff sees all) Member Can See His Feedback",
        responses={
            200: FeedbackSerializer(many=True),
            401: SwaggerErrorResponseSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update feedback record (Admin/Staff sees all)",
        operation_description="Update feedback record (Admin/Staff sees all) Member Can Update His Feedback",
        responses={
            200: FeedbackSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Partial update feedback record (Admin/Staff sees all)",
        operation_description="Partial update feedback record (Admin/Staff sees all) Member Can Partial Update His Feedback",
        responses={
            200: FeedbackSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Destroy feedback record (Admin/Staff sees all)",
        operation_description="Destroy feedback record (Admin/Staff sees all) Member Can Destroy His Feedback",
        responses={
            200: FeedbackSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)    