from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import MembershipPlan
from .serializers import MembershipPlanSerializer
from core.permissions import IsStaffOrAdminAndReadOnly
from rest_framework.permissions import IsAuthenticated
from core.serializers import SwaggerErrorResponseSerializer
from drf_yasg.utils import swagger_auto_schema

class MembershipPlanViewSet(BaseModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    permission_classes = [IsStaffOrAdminAndReadOnly]

    # business logic
    
    # swagger doc
    @swagger_auto_schema(
        operation_summary="Create Membership Plan",
        operation_description="Create Membership Plan. Admin/Staff can create membership plans.",
        responses={
            200:MembershipPlanSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="List Membership Plans",
        operation_description="List Membership Plans. Admin/Staff/Member/anynymus user sees all.",
        responses={
            200:MembershipPlanSerializer(many=True),
            401:SwaggerErrorResponseSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
    @swagger_auto_schema(
        operation_summary="Retrieve Membership Plan",
        operation_description="Retrieve Membership Plan. Admin/Staff/Member/anynymus user sees all.",
        responses={
            200:MembershipPlanSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update Membership Plan",
        operation_description="Update Membership Plan. Admin/Staff can update membership plans.",
        responses={
            200:MembershipPlanSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete Membership Plan",
        operation_description="Delete Membership Plan. Admin/Staff can delete membership plans.",
        responses={
            200:MembershipPlanSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Partial Update Membership Plan",
        operation_description="Partial Update Membership Plan. Admin/Staff can update membership plans.",
        responses={
            200:MembershipPlanSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
        
