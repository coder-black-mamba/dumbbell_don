from core.utils.api_response import success_response
from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import FitnessClass, Booking, Attendance
from .serializers import FitnessClassSerializer, BookingSerializer, AttendanceSerializer,ScheduleSerializer,MemberAttendanceSerializer,MemberBookingSerializer
from .permissions import BookingPermission, IsStaffOrAdminAndReadOnly , IsStuffOrSelfOrReadOnly
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from classes.models import Booking,Attendance  
from users.models import User
from core.serializers import SwaggerErrorResponseSerializer,SwaggerSuccessListResponseSerializer
from drf_yasg.utils import swagger_auto_schema

class FitnessClassViewSet(BaseModelViewSet):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer
    permission_classes = [IsStaffOrAdminAndReadOnly]

    @swagger_auto_schema(
        operation_summary="Create fitness class record",
        operation_description="Create fitness class record (Admin/Staff/Member sees all) Staff Can Add Fitness Class . Member Can View Fitness Class",
        responses={
            200:FitnessClassSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="List fitness class records",
        operation_description="List fitness class records (Admin/Staff/Member sees all) Staff Can Add Fitness Class . Member Can View Fitness Class",
        responses={
            200:FitnessClassSerializer(many=True),
            401:SwaggerErrorResponseSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve fitness class record",
        operation_description="Retrieve fitness class record . Admin/Staff/Member Can Retrieve Any Fitness Class",
        responses={
            200:FitnessClassSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update fitness class record",
        operation_description="Update fitness class record . Only Admin And Staff Can Update Any Fitness Class",
        responses={
            200:FitnessClassSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update fitness class record",
        operation_description="Partial update fitness class record . Only Admin And Staff Can Update Any Fitness Class",
        responses={
            200:FitnessClassSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Destroy fitness class record",
        operation_description="Destroy fitness class record . Only Admin And Staff Can Delete Any Fitness Class",
        responses={
            200:FitnessClassSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)    
 

class BookingViewSet(BaseModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [BookingPermission]
    
    # business logic
    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated and self.request.user.role == User.ADMIN:
            return Booking.objects.all()
        return Booking.objects.filter(member=self.request.user)
    
    def perform_create(self, serializer):
        
        # Create invoice for the booking
        from payments.models import Invoice
        from django.utils import timezone
        from django.db import transaction
        
        try:
            booking = serializer.save(member=self.request.user)
            # with transaction.atomic():
            #     invoice = Invoice.objects.create(
            #         member=self.request.user,
            #         total_cents=booking.fitness_class.price_cents,
            #         due_date=timezone.now() + timezone.timedelta(days=7),  # 7 days from now
            #         status='UNPAID',
            #         metadata={
            #             'booking_id': str(booking.id),
            #             'fitness_class': str(booking.fitness_class.title),
            #             'payment_type': 'booking'
            #         }
            #     )
                # You might want to add more fields to the invoice as needed
        except Exception as e:
            # If invoice creation fails, delete the booking to maintain consistency
            booking.delete()
            raise ValidationError({'error': f'Failed to create invoice: {str(e)}'})

    # for swagger documentation
    @swagger_auto_schema(
        operation_summary="Create booking record ",
        operation_description="Create booking record (Admin/Staff sees all) Member Can Add Booking",
        responses={
            200:MemberBookingSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="List booking records ",
        operation_description="List booking records (Admin/Staff sees all) Member Can See His All Booking",
        responses={
            200:MemberBookingSerializer(many=True),
            401:SwaggerErrorResponseSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve booking record (Admin/Staff sees all)",
        operation_description="Retrieve booking record (Admin/Staff sees all) Member Can See His Booking",
        responses={
            200:MemberBookingSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update booking record",
        operation_description="Update booking record (Admin/Staff sees all) Only Admin Can Update Any Booking",
        responses={
            200:MemberBookingSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update booking record ",
        operation_description="Partial update booking record (Admin/Staff sees all) Only Admin Can Update Any Booking",
        responses={
            200:MemberBookingSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Destroy booking record",
        operation_description="Destroy booking record (Admin/Staff sees all) Only Admin Can Delete Any Booking",
        responses={
            200:MemberBookingSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AttendanceViewSet(BaseModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsStuffOrSelfOrReadOnly]



    # business logic
    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)
    
    def get_queryset(self): 
        if self.request.user and self.request.user.is_authenticated and self.request.user.role == User.ADMIN or self.request.user.role == User.STAFF:
            return Attendance.objects.all()
        return Attendance.objects.filter(booking__member=self.request.user)




    # for swagger documentation
    @swagger_auto_schema(
        operation_summary="Create attendance record",
        operation_description="Create attendance record (Admin/Staff sees all) Staff Can Add Attendence",
        responses={
            200:MemberAttendanceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_summary="List attendance records",
        operation_description="List attendance records (Admin/Staff sees all) Staff Can See All Attendance",
        responses={
            200:MemberAttendanceSerializer(many=True),
            401:SwaggerErrorResponseSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve attendance record",
        operation_description="Retrieve attendance record (Admin/Staff sees all) Staff Can See All Attendance",
        responses={
            200:MemberAttendanceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update attendance record",
        operation_description="Update attendance record (Admin/Staff sees all) ADmin/Staff Can Update Attendence",
        responses={
            200:MemberAttendanceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update attendance record",
        operation_description="Partial update attendance record (Admin/Staff sees all) ADmin/Staff Can Update Attendence",
        responses={
            200:MemberAttendanceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Destroy attendance record",
        operation_description="Destroy attendance record (Admin/Staff sees all) ADmin/Staff Can Delete Attendence",
        responses={
            200:MemberAttendanceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



# simple dunctional omponent for some member info
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    method="get",
    operation_summary="Show Class Schedule",
    operation_description="Show Class Schedule. Admin/Staff sees all, Member sees their own.",
    responses={
        200: ScheduleSerializer(many=True),  
        401: SwaggerErrorResponseSerializer,
    }
)
@api_view(['GET'])
def class_schedule(request):
    data=Booking.objects.filter(member=request.user)
    serializer=ScheduleSerializer(data, many=True)
    return success_response(data=serializer.data)


@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    method="get",
    operation_summary="Show Bookings",
    operation_description="Show Bookings. Admin/Staff sees all, Member sees their own.",
    responses={
        200: MemberBookingSerializer(many=True),  
        401: SwaggerErrorResponseSerializer,
    }
)
@api_view(['GET'])
def bookings(request):
    data=Booking.objects.filter(member=request.user)
    serializer=MemberBookingSerializer(data, many=True)
    return success_response(data=serializer.data)



@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    method="get",
    operation_summary="Show Attendance",
    operation_description="Show Attendance. Admin/Staff sees all, Member sees their own.",
    responses={
        200: MemberAttendanceSerializer(many=True),  
        401: SwaggerErrorResponseSerializer,
    }
)
@api_view(['GET'])
def show_attendance(request):
    if request.user.role == User.ADMIN:  
        data=Attendance.objects.all()
    else:
        data=Attendance.objects.filter(booking__member=request.user)
    serializer=MemberAttendanceSerializer(data, many=True)
    return success_response(data=serializer.data)

