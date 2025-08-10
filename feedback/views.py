from .models import Feedback
from .serializers import FeedbackSerializer
from core.utils.BASEModelViewSet import BaseModelViewSet


class FeedbackViewSet(BaseModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer