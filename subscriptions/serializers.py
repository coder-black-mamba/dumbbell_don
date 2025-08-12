from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id','member','plan', 'start_date', 'end_date', 'status', 'auto_renew']
        read_only_fields = ['id', 'start_date', 'end_date', 'auto_renew', 'member']