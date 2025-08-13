from drf_yasg.utils import swagger_auto_schema
# Create your views here.
from rest_framework import serializers
from rest_framework.response import Response

from core.utils.api_response import success_response

from rest_framework.views import APIView

@swagger_auto_schema(tags=['Test'])
class TestSuccessResponse(APIView):
    def get(self, request):
        return success_response(
            data={"foo": "bar"},
            message="Test successful"
        )
@swagger_auto_schema(tags=['Test'])
class TestInternalServerError(APIView):
    def get(self, request):
        raise Exception("Test Internal Server Error")
@swagger_auto_schema(tags=['Test'])
class TestDivideByZero(APIView):
    def get(self, request):
        return 1 / 0
@swagger_auto_schema(tags=['Test'])
class TestValidationError(APIView):
    def get(self, request):
        raise serializers.ValidationError("Test Validation Error")
