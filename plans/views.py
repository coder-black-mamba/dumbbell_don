from drf_yasg.utils import swagger_auto_schema
from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import MembershipPlan
from .serializers import MembershipPlanSerializer
from core.permissions import IsStaffOrAdminAndReadOnly
from rest_framework.permissions import IsAuthenticated

@swagger_auto_schema(tags=['Membership Plans'])
class MembershipPlanViewSet(BaseModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    permission_classes = [IsAuthenticated,IsStaffOrAdminAndReadOnly]
