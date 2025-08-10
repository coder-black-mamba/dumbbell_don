from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import MembershipPlan
from .serializers import MembershipPlanSerializer
from core.permissions import IsStaffOrAdminAndReadOnly
from rest_framework.permissions import IsAuthenticated

class MembershipPlanViewSet(BaseModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    permission_classes = [IsAuthenticated,IsStaffOrAdminAndReadOnly]
