from rest_framework.viewsets import ModelViewSet
from .models import BaseReport, MembershipReport, AttendanceReport, FeedbackReport
from .serializers import BaseReportSerializer, MembershipReportSerializer, AttendanceReportSerializer, FeedbackReportSerializer
from core.utils.BASEModelViewSet import BaseModelViewSet
# Create your views here.
class MembershipReportViewSet(BaseModelViewSet):
    queryset = MembershipReport.objects.all()
    serializer_class = MembershipReportSerializer

class AttendanceReportViewSet(BaseModelViewSet):
    queryset = AttendanceReport.objects.all()
    serializer_class = AttendanceReportSerializer

class FeedbackReportViewSet(BaseModelViewSet):
    queryset = FeedbackReport.objects.all()
    serializer_class = FeedbackReportSerializer

