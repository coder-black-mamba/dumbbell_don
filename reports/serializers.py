from rest_framework import serializers
from .models import BaseReport, MembershipReport, AttendanceReport, FeedbackReport

class BaseReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseReport
        fields = '__all__'


class MembershipReportSerializer(BaseReportSerializer):
    class Meta:
        model = MembershipReport
        fields = '__all__'

class AttendanceReportSerializer(BaseReportSerializer):
    class Meta:
        model = AttendanceReport
        fields = '__all__'
class FeedbackReportSerializer(BaseReportSerializer):
    class Meta:
        model = FeedbackReport
        fields = '__all__'  