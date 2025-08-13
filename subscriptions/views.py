from .models import Subscription
from .serializers import SubscriptionSerializer
from core.utils.BASEModelViewSet import BaseModelViewSet 
from subscriptions.permissions import IsSubscriptionOwner
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from core.serializers import SwaggerErrorResponseSerializer

class SubscriptionViewSet(BaseModelViewSet): 
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsSubscriptionOwner]
    # business logic
    def get_queryset(self):
        return Subscription.objects.filter(member=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(member=self.request.user)

    # swagger doc
    @swagger_auto_schema(
        operation_summary="Create Subscription",
        operation_description="Create Subscription. Admin/Staff can create for any member, Member can create for themselves.",
        responses={
            201: SubscriptionSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="List Subscriptions",
        operation_description="List Subscriptions. Admin/Staff can list for any member, Member can list for themselves.",
        responses={
            200: SubscriptionSerializer(many=True),
            401: SwaggerErrorResponseSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Retrieve Subscription",
        operation_description="Retrieve Subscription. Admin/Staff can retrieve for any member, Member can retrieve for themselves.",
        responses={
            200: SubscriptionSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update Subscription",
        operation_description="Update Subscription. Admin update for any member, Staff/Member can not update for subscription.",
        responses={
            200: SubscriptionSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Partial Update Subscription",
        operation_description="Partial Update Subscription. Admin update for any member, Staff/Member can not update for subscription.",
        responses={
            200: SubscriptionSerializer,
            401: SwaggerErrorResponseSerializer,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Subscription",
        operation_description="Delete Subscription. Admin delete for any member, Staff/Member can not delete for subscription.",
        responses={
            204: openapi.Response(description="No Content"),
            401: SwaggerErrorResponseSerializer,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)