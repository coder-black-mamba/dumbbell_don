from rest_framework import serializers
from .models import FitnessClass, Booking, Attendance, FitnessClass
from users.models import User
from users.serializers import UserSimpleSerializer

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at','created_by']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'member', 'fitness_class', 'status','booked_at']
        read_only_fields = ['id', 'created_at', 'updated_at','member','booked_at','status']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at','marked_by','marked_at']
    
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

class MemberInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class MemberFitnessClassSerializer(serializers.ModelSerializer):
    instructor = MemberInstructorSerializer(read_only=True)
    class Meta:
        model = FitnessClass
        fields = ['title', 'description', 'instructor']


class MemberBookingSerializer(serializers.ModelSerializer):
    class_data = MemberFitnessClassSerializer(source='fitness_class', read_only=True)
    class Meta:
        model = Booking
        fields = ['member','class_data'] 


class MemberAttendanceSerializer(serializers.ModelSerializer):
    booking_data = MemberBookingSerializer(source='booking', read_only=True)
    class Meta:
        model = Attendance
        fields = ['present','booking_data','marked_by','marked_at']