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
from django.conf import settings as main_settings
import uuid
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from core.serializers import SwaggerErrorResponseSerializer
from rest_framework.decorators import api_view
from sslcommerz_lib import SSLCOMMERZ
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect



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
        


@swagger_auto_schema(
    method='post',
    operation_description="Initiate a payment session with SSLCommerz",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['invoice_id'],
        properties={
            'invoice_id': openapi.Schema(type=openapi.TYPE_STRING, description='Invoice ID for the payment'),
        },
    ),
    responses={
        200: openapi.Response(
            description='Payment initialization successful',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'payment_url': openapi.Schema(type=openapi.TYPE_STRING, description='URL to redirect for payment')
                }
            )
        ),
        400: 'Invalid request data',
        401: 'Authentication credentials were not provided',
    }
)

@api_view(['POST'])
@login_required
def initiate_payment(request):
    try:
        user = request.user
        invoice_id = request.data.get("invoice_id")
        invoice = Invoice.objects.get(number=invoice_id)
        
        # check if invoice is already paid
        if invoice.status == 'PAID':
            return Response({'error': 'Invoice already paid'}, status=status.HTTP_400_BAD_REQUEST)
        

        # create a payment iobject also 
        payment = Payment.objects.create(
            invoice=invoice,
            member=user,
            amount_cents=invoice.total_cents,
            currency="USD",
            status="PENDING",
            reference=str(uuid.uuid4()),
            metadata={"invoice": str(invoice.number),"payment_type": invoice.metadata.get('payment_type'),"booking_id": invoice.metadata.get('booking_id')}
        )
    

        amount = invoice.total_cents

        settings = {'store_id': main_settings.STORE_ID,
                    'store_pass': main_settings.STORE_PASSWORD, 'issandbox': True}
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = amount/100
        post_body['currency'] = "USD"
        post_body['tran_id'] = f"txn_{invoice.number}"
        post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
        post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
        post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
        post_body['emi_option'] = 0
        post_body['cus_name'] = f"{user.first_name} {user.last_name}"
        post_body['cus_email'] = user.email
        post_body['cus_phone'] ="+8801717963289"
        post_body['cus_add1'] = user.address if user.address else "Dhaka"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "E-commerce Products"
        post_body['product_category'] = "General"
        post_body['product_profile'] = "general"
        post_body['ship_name'] = f"{user.first_name} {user.last_name}"
        post_body['ship_email'] = user.email
        post_body['ship_add1'] = user.address if user.address else "Dhaka"
        post_body['ship_city'] = "Dhaka"
        post_body['ship_country'] = "Bangladesh"
        post_body['ship_phone'] = "+8801717963289"
        post_body['ship_postcode'] = "1207"

        response = sslcz.createSession(post_body)  # API response
        # print(response)
        if response.get("status") == 'SUCCESS':
            return Response({"payment_url": response['GatewayPageURL']})
        return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Handle successful payment callback from SSLCommerz",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'tran_id': openapi.Schema(type=openapi.TYPE_STRING, description='Transaction ID from SSLCommerz')
        },
        required=['tran_id']
    ),
    responses={
        302: 'Redirects to frontend dashboard page on success',
        400: 'Invalid transaction ID',
        404: 'Invoice not found'
    }
)
@api_view(['POST'])
def payment_success(request):
    print("Inside success")
    try:
        invoice_id = request.data.get("tran_id").split('_')[1]
        invoice = Invoice.objects.get(number=invoice_id)
        invoice.status = "PAID"
        invoice.save()
        payment = Payment.objects.get(invoice=invoice)
        payment.status = "PAID"
        payment.save()
        # print("Payment success",f"{main_settings.FRONTEND_URL}/payment-success/")
        return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/payment/success/")
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Handle cancelled payment from SSLCommerz",
    responses={
        302: 'Redirects to frontend dashboard page'
    }
)
@api_view(['POST'])
def payment_cancel(request):
    try:
        return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/payment/cancel/")
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Handle failed payment from SSLCommerz",
    responses={
        302: 'Redirects to frontend dashboard page'
    }
)
@api_view(['POST'])
def payment_fail(request):
    try:
        print("Inside fail")
        return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/payment/fail/")
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

