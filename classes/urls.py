from django.urls import path, include
from .views import class_schedule, bookings,show_attendance

urlpatterns = [
    path('schedule/', class_schedule),
    path('bookings/', bookings),
    path('attendance/', show_attendance),
]