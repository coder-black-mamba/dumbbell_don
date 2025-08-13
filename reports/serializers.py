from rest_framework import serializers
from feedback.models import Feedback
from subscriptions.models import Subscription

class FeedbackReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feedback
        fields=["member","fitness_class","rating","comment"]


class SubscriptionReportSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Subscription
        fields=["member","plan","status","auto_renew","start_date","end_date"]
    