from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import FitnessClass, Booking, Attendance
from .serializers import FitnessClassSerializer, BookingSerializer, AttendanceSerializer

class FitnessClassViewSet(BaseModelViewSet):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer


class BookingViewSet(BaseModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    # def get_queryset(self):
    #     return Booking.objects.filter(member=self.request.user)


class AttendanceViewSet(BaseModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    # def get_queryset(self):
    #     return Attendance.objects.filter(booking__member=self.request.user)

