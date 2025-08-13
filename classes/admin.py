from django.contrib import admin
from .models import FitnessClass, Booking, Attendance
# Register your models here.
admin.site.register(FitnessClass)
admin.site.register(Booking)
admin.site.register(Attendance)