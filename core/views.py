# Create your views here.
from rest_framework import serializers
from rest_framework.response import Response

from core.utils.api_response import success_response
from core.serializers import SwaggerErrorResponseSerializer,SwaggerSuccessResponseSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

class TestSuccessResponse(APIView):
    """
    This endpoint is used to test the success response
    """ 
    @swagger_auto_schema(
        operation_summary="Test Success Response",
        operation_description="Returns a success response for testing purposes.",
        responses={
            200:SwaggerSuccessResponseSerializer,
            500:SwaggerErrorResponseSerializer,
        }
    )
    def get(self, request):
        return success_response(
            data={"foo": "bar"},
            message="Test successful"
        )



class TestInternalServerError(APIView):
    """
    This endpoint is used to test the internal server error
    """  
    @swagger_auto_schema(
        operation_summary="Test Internal Server Error",
        operation_description="Raises an internal server error for testing purposes.",
        responses={
            500:SwaggerErrorResponseSerializer,
            200:SwaggerSuccessResponseSerializer,
        }
    )
    def get(self, request):
        raise Exception("Test Internal Server Error")


class TestDivideByZero(APIView):
    """
    This endpoint is used to test the divide by zero error
    """ 
    @swagger_auto_schema(
        operation_summary="Test Divide By Zero Error",
        operation_description="Raises a divide by zero error for testing purposes.",
        responses={
            500:SwaggerErrorResponseSerializer,
            200:SwaggerSuccessResponseSerializer,
        }
    )
    def get(self, request):
        return 1 / 0
class TestValidationError(APIView):
    """
    This endpoint is used to test the validation error
    """ 
    @swagger_auto_schema(
        operation_summary="Test Validation Error",
        operation_description="Raises a validation error for testing purposes.",
        responses={
            500:SwaggerErrorResponseSerializer,
            200:SwaggerSuccessResponseSerializer,
        }
    )
    def get(self, request):
        raise serializers.ValidationError("Test Validation Error")
