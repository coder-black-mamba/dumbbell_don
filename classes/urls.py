from django.urls import path, include
from .views import class_schedule, bookings

urlpatterns = [
    path('schedule/', class_schedule),
    path('bookings/', bookings),
]