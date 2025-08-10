from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import MembershipPlan
from .serializers import MembershipPlanSerializer


class MembershipPlanViewSet(BaseModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
