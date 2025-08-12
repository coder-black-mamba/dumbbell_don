from rest_framework import serializers
from .models import FitnessClass, Booking, Attendance

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at','created_by']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'member', 'fitness_class', 'status','booked_at']
        read_only_fields = ['id', 'created_at', 'updated_at','member','booked_at']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
    