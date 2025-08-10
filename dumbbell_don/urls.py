"""
URL configuration for dumbbell_don project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.http import HttpResponse,JsonResponse
from django.conf.urls import handler400,handler403,handler404,handler500

def hello_world(request):
    return HttpResponse("Hello, world!")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", hello_world),
    path("core/", include("core.urls")),
    path("api/v1/", include("api.urls")),
]  + debug_toolbar_urls()

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

handler400 = custom_handler400

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

handler403 = custom_handler403

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

handler404 = custom_handler404

def custom_handler500(request):
    return JsonResponse({
        "success": False,
        "status": 500,
        "message": "Internal Server Error",
        "errors": {},
        "code": "internal_server_error"
    }, status=500)

handler500 = custom_handler500