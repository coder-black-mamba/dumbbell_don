from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()
    member_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Feedback
        fields = [
            'id', 'member', 'member_name', 'member_image', 
            'fitness_class', 'rating', 'comment', 
            'created_at', 'updated_at', 'generated_by'
        ]
        read_only_fields = [
            'id', 'member', 'member_name', 'member_image', 
            'created_at', 'updated_at', 'generated_by'
        ]
    
    def get_member_name(self, obj):
        return f"{obj.member.first_name} {obj.member.last_name}" if obj.member else None
    
    def get_member_image(self, obj):
        if obj.member and hasattr(obj.member, 'profile_picture') and obj.member.profile_picture:
            return obj.member.profile_picture.url
        return None
    