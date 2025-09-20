from rest_framework import serializers
from .models import Feedback
from users.serializers import UserSerializer, UserSimpleSerializer

class FeedbackSerializer(serializers.ModelSerializer):
    member = UserSimpleSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['id','member', 'created_at', 'updated_at','generated_by']
    