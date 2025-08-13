from drf_yasg.utils import swagger_auto_schema
from core.utils.api_response import success_response
from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import FitnessClass, Booking, Attendance
from .serializers import FitnessClassSerializer, BookingSerializer, AttendanceSerializer,ScheduleSerializer,MemberAttendanceSerializer,MemberBookingSerializer
from .permissions import IsStaffOrAdminAndReadOnly , IsStuffOrSelfOrReadOnly
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from classes.models import Booking,Attendance  
from users.models import User

class FitnessClassViewSet(BaseModelViewSet):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer
    permission_classes = [IsStaffOrAdminAndReadOnly]
 
@swagger_auto_schema(tags=['Bookings'])
class BookingViewSet(BaseModelViewSet):
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN:
            return Booking.objects.all()
        return Booking.objects.filter(member=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(member=self.request.user)

@swagger_auto_schema(tags=['Attendance'])
class AttendanceViewSet(BaseModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsStuffOrSelfOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN or self.request.user.role == User.STAFF:
            return Attendance.objects.all()
        return Attendance.objects.filter(booking__member=self.request.user)



# simple dunctional omponent for some member info
@swagger_auto_schema(method='get', tags=['Member Info'])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def class_schedule(request):
    data=Booking.objects.filter(member=request.user)
    serializer=ScheduleSerializer(data, many=True)
    return success_response(data=serializer.data)


@swagger_auto_schema(method='get', tags=['Member Info'])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def bookings(request):
    data=Booking.objects.filter(member=request.user)
    serializer=MemberBookingSerializer(data, many=True)
    return success_response(data=serializer.data)



@swagger_auto_schema(method='get', tags=['Member Info'])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def show_attendance(request):
    if request.user.role == User.ADMIN:  
        data=Attendance.objects.all()
    else:
        data=Attendance.objects.filter(booking__member=request.user)
    serializer=MemberAttendanceSerializer(data, many=True)
    return success_response(data=serializer.data)

