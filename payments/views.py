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
from core.serializers import SwaggerErrorResponseSerializer

class InvoiceViewSet(BaseModelViewSet):
    
    # queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminOrSelf]
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN:
            return Invoice.objects.all()
        return Invoice.objects.filter(member=self.request.user)
    # business logic
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

    # swagger doc
    @swagger_auto_schema(
        operation_summary="Create Invoice",
        operation_description="Create Invoice. Admin/Staff/Member can create invoice for subscription or booking.",
        responses={
            200:InvoiceSerializer,
            401:SwaggerErrorResponseSerializer,
        },
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

    @swagger_auto_schema(
        operation_summary="List Invoices",
        operation_description="List Invoices. Admin/Staff can list All invoices. Member can list their own invoices.",
        responses={
            200:InvoiceSerializer(many=True),
            401:SwaggerErrorResponseSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Retrieve Invoice",
        operation_description="Retrieve Invoice. Admin/Staff can retrieve all invoices. Member can retrieve their own invoices.",
        responses={
            200:InvoiceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)   
    
    @swagger_auto_schema(
        operation_summary="Update Invoice",
        operation_description="Update Invoice. Admin can update all invoices. Staff only see all invoices and member can view only his own invoices.",
        responses={
            200:InvoiceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Invoice",
        operation_description="Delete Invoice. Admin can delete all invoices. Staff only see all invoices and member can view only his own invoices.",
        responses={
            200:InvoiceSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary="Partial Update Invoice",
        operation_description="Partial Update Invoice. Admin can update all invoices. Staff only see all invoices and member can view only his own invoices.",
        responses={
            200:InvoiceSerializer(many=True),
            401:SwaggerErrorResponseSerializer,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)





class PaymentViewSet(BaseModelViewSet):
    #    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrSelf]

    # business logic
    
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

    
    # swagger doc
    @swagger_auto_schema(
        operation_summary="List Payments",
        operation_description="List Payments. Admin/Staff can list All payments. Member can list their own payments.",
        responses={
            200:PaymentSerializer(many=True),
            401:SwaggerErrorResponseSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)   
    
    @swagger_auto_schema(
        operation_summary="Retrieve Payment",
        operation_description="Retrieve Payment. Admin/Staff can retrieve all payments. Member can retrieve their own payments.",
        responses={
            200:PaymentSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)   
    
    @swagger_auto_schema(
        operation_summary="Update Payment",
        operation_description="Update Payment. Admin can update all payments. Staff only see all payments and member can view only his own payments.",
        responses={
            200:PaymentSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @swagger_auto_schema(
        operation_summary="Delete Payment",
        operation_description="Delete Payment. Admin can delete all payments. Staff only see all payments and member can view only his own payments.",
        responses={
            200:PaymentSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)   
    
    @swagger_auto_schema(
        operation_summary="Partial Update Payment",
        operation_description="Partial Update Payment. Admin can update all payments. Staff only see all payments and member can view only his own payments.",
        responses={
            200:PaymentSerializer(many=True),
            401:SwaggerErrorResponseSerializer,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Payment",
        operation_description="Create Payment. Member can create payments through invoices .",
        responses={
            200:PaymentSerializer,
            401:SwaggerErrorResponseSerializer,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        
        