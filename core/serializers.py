from rest_framework import serializers
from classes.serializers import MemberAttendanceSerializer
# swagger serializers
class SwaggerSuccessResponseSerializer(serializers.Serializer):
    """
    This serializer is used to serialize the success response
    """
    success = serializers.BooleanField(default=True)
    status = serializers.IntegerField(default=200)
    message = serializers.CharField(default="Test successful")
    data = serializers.DictField(default={"foo": "bar"})
    meta = serializers.DictField(default={})


class SwaggerErrorResponseSerializer(serializers.Serializer):
    """
    This serializer is used to serialize the error response
    """
    success = serializers.BooleanField(default=False)
    status = serializers.IntegerField(default=500)
    message = serializers.CharField(default="Internal Server Error")
    errors = serializers.DictField(default={})



class SwaggerSuccessListResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    status = serializers.IntegerField(default=200)
    message = serializers.CharField(default="Request successful")
    data = MemberAttendanceSerializer(many=True)
    meta = serializers.DictField(default={})


class SwaggerErrorResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=False)
    status = serializers.IntegerField(default=401)
    message = serializers.CharField(default="Unauthorized")
    errors = serializers.DictField(default={})
