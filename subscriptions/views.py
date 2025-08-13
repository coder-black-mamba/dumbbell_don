from drf_yasg.utils import swagger_auto_schema
from .models import Subscription
from .serializers import SubscriptionSerializer
from core.utils.BASEModelViewSet import BaseModelViewSet 
from subscriptions.permissions import IsSubscriptionOwner
from rest_framework.permissions import IsAuthenticated

@swagger_auto_schema(tags=['Subscriptions'])
class SubscriptionViewSet(BaseModelViewSet): 
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsSubscriptionOwner]

    def get_queryset(self):
        return Subscription.objects.filter(member=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(member=self.request.user)