from django.urls import path
from . import views

urlpatterns = [
    path("test-success-response/", views.TestSuccessResponse.as_view(), name="test-success-response"),
    path("test-internal-server-error/", views.TestInternalServerError.as_view(), name="test-internal-server-error"),
    path("test-divide-by-zero/", views.TestDivideByZero.as_view(), name="test-divide-by-zero"),
    path("test-validation-error/", views.TestValidationError.as_view(), name="test-validation-error"),
]