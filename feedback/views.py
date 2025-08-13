from drf_yasg.utils import swagger_auto_schema
from .models import Feedback
from .serializers import FeedbackSerializer
from core.utils.BASEModelViewSet import BaseModelViewSet
from .permissions import IsAdminOrSelfOrReadOnly
from users.models import User

@swagger_auto_schema(tags=['Feedback'])
class FeedbackViewSet(BaseModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOrSelfOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN:
            return Feedback.objects.all()
        if self.request.user.role == User.STAFF:
            return Feedback.objects.filter(fitness_class__instructor=self.request.user)
        return Feedback.objects.all()
    
    def get_object(self):
        if self.request.user.role == User.ADMIN:
            return super().get_object()
        return Feedback.objects.get(member=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(member=self.request.user) 