from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import FitnessClass, Booking, Attendance
from .serializers import FitnessClassSerializer, BookingSerializer, AttendanceSerializer
from .permissions import IsStaffOrAdminAndReadOnly

class FitnessClassViewSet(BaseModelViewSet):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer
    permission_classes = [IsStaffOrAdminAndReadOnly]


class BookingViewSet(BaseModelViewSet):
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.filter(member=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(member=self.request.user)


class AttendanceViewSet(BaseModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    # def get_queryset(self):
    #     return Attendance.objects.filter(booking__member=self.request.user)

