from django.urls import path, include
from .views import class_schedule

urlpatterns = [
    path('schedule/', class_schedule),
]