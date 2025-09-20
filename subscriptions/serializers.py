from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    plan_title = serializers.CharField(source='plan.name', read_only=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'member', 'plan', 'plan_title', 'start_date', 'end_date', 'status', 'auto_renew']
        read_only_fields = ['id', 'start_date', 'status', 'end_date', 'auto_renew', 'member', 'plan_title']