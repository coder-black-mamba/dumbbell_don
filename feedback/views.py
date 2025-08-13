from .models import Feedback
from .serializers import FeedbackSerializer
from core.utils.BASEModelViewSet import BaseModelViewSet
from .permissions import IsAdminOrSelfOrReadOnly
from users.models import User

class FeedbackViewSet(BaseModelViewSet):
    # queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOrSelfOrReadOnly]
    
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