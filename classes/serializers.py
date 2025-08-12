from rest_framework import serializers
from .models import FitnessClass, Booking, Attendance
from users.models import User

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
    
class ScheduleInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class ScheduleFitnessClassSerializer(serializers.ModelSerializer):
    instructor = ScheduleInstructorSerializer(read_only=True)
    class Meta:
        model = FitnessClass
        fields = ['id','title', 'description', 'instructor', 'start_datetime', 'end_datetime', 'duration_minutes', 'location']


class ScheduleSerializer(serializers.ModelSerializer):
    fitness_class = ScheduleFitnessClassSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = ['id', 'member', 'status','booked_at','fitness_class'] 

        