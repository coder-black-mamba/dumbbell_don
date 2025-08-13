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
from django.urls import path,re_path
from django.urls import include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.http import HttpResponse,JsonResponse
from django.conf.urls import handler400,handler403,handler404,handler500
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
import re
from core.custom_basic_error_handler import custom_handler400, custom_handler403, custom_handler404, custom_handler500

def hello_world(request):
    return HttpResponse("Hello, world!")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", hello_world),
    path("core/", include("core.urls")),
    path("api/v1/", include("api.urls")),
] + debug_toolbar_urls()

schema_view = get_schema_view(
   openapi.Info(
      title="Dumbbell Don Gym Management API",
      default_version='v1',
      description="Dumbbell Don Gym Management API",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="sde.sayed24@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    # Your existing urls

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


# custom basic error handlers
handler400 = custom_handler400
handler403 = custom_handler403
handler404 = custom_handler404
handler500 = custom_handler500








