from django.http import JsonResponse
# customizing default error handlers to return json response instead of html 
def custom_handler400(request, exception):
     return JsonResponse({
        "success": False,
        "status": 400,
        "message": "Resource not found",
        "errors": {
            "non_field_errors": ["The requested resource was not found."]
        },
        "code": "not_found"
    }, status=400)


def custom_handler403(request, exception):
    return JsonResponse({
        "success": False,
        "status": 403,
        "message": "Forbidden",
        "errors": {
            "non_field_errors": ["You do not have permission to perform this action."]
        },
        "code": "forbidden"
    }, status=403)


def custom_handler404(request, exception):
    return JsonResponse({
        "success": False,
        "status": 404,
        "message": "Resource not found",
        "errors": {
            "non_field_errors": ["The requested resource was not found."]
        },
        "code": "not_found"
    }, status=404)

def custom_handler500(request):
    return JsonResponse({
        "success": False,
        "status": 500,
        "message": "Internal Server Error",
        "errors": {},
        "code": "internal_server_error"
    }, status=500)  