from core.utils.api_response import success_response
from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import FitnessClass, Booking, Attendance
from .serializers import FitnessClassSerializer, BookingSerializer, AttendanceSerializer,ScheduleSerializer,MemberAttendanceSerializer,MemberBookingSerializer
from .permissions import BookingPermission, IsStaffOrAdminAndReadOnly , IsStuffOrSelfOrReadOnly
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from classes.models import Booking,Attendance  
from users.models import User
from core.serializers import SwaggerErrorResponseSerializer
from drf_yasg.utils import swagger_auto_schema

class FitnessClassViewSet(BaseModelViewSet):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer
    permission_classes = [IsStaffOrAdminAndReadOnly]
 

class BookingViewSet(BaseModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [BookingPermission]
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN:
            return Booking.objects.all()
        return Booking.objects.filter(member=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(member=self.request.user)


class AttendanceViewSet(BaseModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsStuffOrSelfOrReadOnly]



    # business logic
    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)
    
    def get_queryset(self): 
        if self.request.user.role == User.ADMIN or self.request.user.role == User.STAFF:
            return Attendance.objects.all()
        return Attendance.objects.filter(booking__member=self.request.user)




    # for swagger documentation
    @swagger_auto_schema(
        operation_summary="Create attendance record (Admin/Staff sees all)",
        operation_description="Create attendance record (Admin/Staff sees all) Staff Can Add Attendence",
        responses={
            200:MemberAttendanceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_summary="List attendance records (Admin/Staff sees all)",
        operation_description="List attendance records (Admin/Staff sees all) Staff Can See All Attendance",
        responses={
            200:MemberAttendanceSerializer(many=True),
            401:SwaggerErrorResponseSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve attendance record (Admin/Staff sees all)",
        operation_description="Retrieve attendance record (Admin/Staff sees all) Staff Can See All Attendance",
        responses={
            200:MemberAttendanceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update attendance record (Admin/Staff sees all)",
        operation_description="Update attendance record (Admin/Staff sees all) Staff Can Update Attendence",
        responses={
            200:MemberAttendanceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update attendance record (Admin/Staff sees all)",
        operation_description="Partial update attendance record (Admin/Staff sees all) Staff Can Update Attendence",
        responses={
            200:MemberAttendanceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Destroy attendance record (Admin/Staff sees all)",
        operation_description="Destroy attendance record (Admin/Staff sees all) Staff Can Delete Attendence",
        responses={
            200:MemberAttendanceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



# simple dunctional omponent for some member info
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def class_schedule(request):
    data=Booking.objects.filter(member=request.user)
    serializer=ScheduleSerializer(data, many=True)
    return success_response(data=serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def bookings(request):
    data=Booking.objects.filter(member=request.user)
    serializer=MemberBookingSerializer(data, many=True)
    return success_response(data=serializer.data)



@permission_classes([IsAuthenticated])
@api_view(['GET'])
def show_attendance(request):
    if request.user.role == User.ADMIN:  
        data=Attendance.objects.all()
    else:
        data=Attendance.objects.filter(booking__member=request.user)
    serializer=MemberAttendanceSerializer(data, many=True)
    return success_response(data=serializer.data)

