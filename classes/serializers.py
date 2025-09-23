from rest_framework import serializers
from .models import FitnessClass, Booking, Attendance, FitnessClass
from users.models import User
from users.serializers import UserSimpleSerializer
from django.db import transaction
from rest_framework.exceptions import ValidationError

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at','created_by']


class BookingSerializer(serializers.ModelSerializer):
    member = UserSimpleSerializer(read_only=True)
    fitness_class = FitnessClassSerializer(read_only=True)

    # Extra write-only fields for creation
    member_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="member",
        write_only=True
    )
    fitness_class_id = serializers.PrimaryKeyRelatedField(
        queryset=FitnessClass.objects.all(),
        source="fitness_class",
        write_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id', 
            'member', 
            'fitness_class', 
            'status', 
            'booked_at',
            'member_id',      # for input
            'fitness_class_id' # for input
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'booked_at']

    def create(self, validated_data):
        # member and fitness_class will already be resolved by PrimaryKeyRelatedField
        booking = Booking.objects.create(**validated_data)
        return booking

class AttendanceSerializer(serializers.ModelSerializer):
    booking_data = BookingSerializer(source='booking', read_only=True)
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at','marked_by','marked_at','booking_data','fitness_class']
    
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
        fields = ['title', 'description', 'instructor','start_datetime','end_datetime']


class MemberBookingSerializer(serializers.ModelSerializer):
    class_data = MemberFitnessClassSerializer(source='fitness_class', read_only=True)
    class Meta:
        model = Booking
        fields = ['member','class_data','fitness_class','status','booked_at'] 



class MemberAttendanceSerializer(serializers.ModelSerializer):
    booking_data = MemberBookingSerializer(source='booking', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['present', 'booking_data', 'marked_by', 'marked_at']
        read_only_fields = ['marked_by', 'marked_at']
    
    def validate(self, attrs):
        # Get the booking from the request data or context
        booking_id = self.context.get('request').data.get('booking')
        if not booking_id:
            raise ValidationError({'booking': 'This field is required.'})
        
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            raise ValidationError({'booking': 'Invalid booking ID.'})
            
        # Check if attendance already exists for this booking
        if Attendance.objects.filter(booking=booking).exists():
            raise ValidationError({'booking': 'Attendance already marked for this booking.'})
            
        # Check if booking status is valid for attendance
        if booking.status != 'BOOKED':
            raise ValidationError({'booking': f'Cannot mark attendance for a booking with status: {booking.status}'})
            
        attrs['booking'] = booking
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')
        booking = validated_data.pop('booking', None)
        
        if not booking:
            raise ValidationError({'booking': 'Booking is required.'})
            
        # Mark the user who is recording the attendance
        validated_data['marked_by'] = request.user if request and hasattr(request, 'user') else None
        
        # Create the attendance record
        attendance = Attendance.objects.create(booking=booking, **validated_data)
        
        # Update the booking status if present is True
        if attendance.present:
            booking.status = 'ATTENDED'
            booking.save(update_fields=['status', 'updated_at'])
            
        return attendance