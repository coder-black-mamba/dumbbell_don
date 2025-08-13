from django.forms import ValidationError
from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer
from users.models import User
from subscriptions.models import Subscription
from classes.models import Booking
from rest_framework import status
from core.utils.api_response import error_response
from core.permissions import IsAdminOrSelf
import uuid
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
 
class InvoiceViewSet(BaseModelViewSet):
    
    # queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminOrSelf]
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN:
            return Invoice.objects.all()
        return Invoice.objects.filter(member=self.request.user)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'payment_type',
                openapi.IN_QUERY,
                description="Type of payment",
                type=openapi.TYPE_STRING,
                required=False,
                enum=["subscription", "booking", "other"]
            ),
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description="Subscription ID or Booking ID for payment",
                type=openapi.TYPE_STRING,
                required=False
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def perform_create(self, serializer):

        payment_type=self.request.query_params.get('payment_type')
        id=self.request.query_params.get('id')
        
        if payment_type == 'subscription':
            subscription_data = Subscription.objects.get(member=self.request.user, id=id)
            metadata={"subscription": str(subscription_data.plan),"payment_type": "subscription","subscription_id": subscription_data.id}

            serializer.save(member=self.request.user, total_cents=subscription_data.plan.price_cents, metadata=metadata)
        elif payment_type == 'booking':
            booking_data = Booking.objects.get(id=id)
            metadata={"booking": str(booking_data),"payment_type": "booking","booking_id": booking_data.id}
            serializer.save(member=self.request.user, total_cents=booking_data.fitness_class.price_cents, metadata=metadata)
        else:
            serializer.save(member=self.request.user, total_cents=0, metadata={"other": "Empty Invoice"})





class PaymentViewSet(BaseModelViewSet):
    #    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrSelf]
    
    def perform_create(self, serializer):
        invoice = Invoice.objects.get(id=self.request.data.get('invoice'))
        payment_type=invoice.metadata.get('payment_type')
        
        

        


        if invoice.status == 'PAID':
            raise ValidationError('Invoice already paid' )
            return 

        if invoice.total_cents <=0:
            raise ValidationError('Invoice total is less than or equal to 0')
            return 
        

        # updating subscription and booking status
        if payment_type == 'subscription':
            subscription_data = Subscription.objects.get(member=self.request.user, id=invoice.metadata.get('subscription_id'))
            subscription_data.status = 'ACTIVE'
            subscription_data.save()

            invoice.status = 'PAID'
            invoice.save()
            serializer.save(member=self.request.user,amount_cents=invoice.total_cents,status='PAID',reference=str(uuid.uuid4()),paid_at=timezone.now(),metadata={"invoice": str(invoice.number),"payment_type": payment_type,"subscription":str(subscription_data.plan),"subscription_id": subscription_data.id}) 

        elif payment_type == 'booking':
            booking_data = Booking.objects.get(id=invoice.metadata.get('booking_id'))
            booking_data.status = 'ATTENDED'
            booking_data.save()

            invoice.status = 'PAID'
            invoice.save()
            serializer.save(member=self.request.user,amount_cents=invoice.total_cents,status='PAID',reference=str(uuid.uuid4()),paid_at=timezone.now(),metadata={"invoice": str(invoice.number),"payment_type": payment_type,"booking":str(booking_data),"booking_id": booking_data.id}) 
        
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN or self.request.user.role == User.STAFF:
            return Payment.objects.all()
        return Payment.objects.filter(member=self.request.user)