from rest_framework import serializers
from feedback.models import Feedback

class FeedbackReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feedback
        fields=["member","fitness_class","rating","comment"]