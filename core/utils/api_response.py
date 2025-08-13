from rest_framework.response import Response

def success_response(data=None, message="Success", status_code=200, meta=None):
    return Response({
        "success": True,
        "status": status_code,
        "message": message,
        "data": data if data is not None else {},
        "meta": meta if meta is not None else {}
    }, status=status_code)

def error_response(message="Something went wrong", status_code=500):
    return Response({
        "success": False,
        "status": status_code,
        "message": message,
        "data": {},
        "meta": {}
    }, status=status_code)
    