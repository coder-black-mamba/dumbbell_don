# Create your views here.
from rest_framework import serializers
from rest_framework.response import Response

from core.utils.api_response import success_response

from rest_framework.views import APIView

class TestSuccessResponse(APIView):
    def get(self, request):
        return success_response(
            data={"foo": "bar"},
            message="Test successful"
        )
class TestInternalServerError(APIView):
    def get(self, request):
        raise Exception("Test Internal Server Error")
class TestDivideByZero(APIView):
    def get(self, request):
        return 1 / 0
class TestValidationError(APIView):
    def get(self, request):
        raise serializers.ValidationError("Test Validation Error")
