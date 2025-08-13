from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status as drf_status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        status_code=response.status_code
        detail=response.data



        # for normilized error message means is details exsts then extract the message from detail other wise this will be a validation error
        message = detail.get("detail") if isinstance (detail, dict) else "Validation Error"
        
        # serializers and validators errors handels differently so lets tackle them
        if isinstance(detail, dict):
            errors = {k: v for k, v in detail.items() if k != "detail"}
        else:
            errors = {"non_field_errors":[str(detail)]}

            
        return Response({
            "success": False,
            "status": status_code,
            "message": message,
            "errors": errors,
        }, status=status_code)
    # if response is not None means it is a drf exception 500 internal server error
    return Response({
        "success": False,
        "status": drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "Internal Server Error",
        "errors": {},
    }, status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR)
