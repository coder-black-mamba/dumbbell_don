from core.utils.BASEModelViewSet import BaseModelViewSet
from .models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer
from users.models import User
from subscriptions.models import Subscription
from rest_framework.response import Response
from rest_framework import status
from core.utils.api_response import error_response
from core.permissions import IsAdminOrSelf
import uuid
from django.utils import timezone

class InvoiceViewSet(BaseModelViewSet):
    # queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminOrSelf]
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN:
            return Invoice.objects.all()
        return Invoice.objects.filter(member=self.request.user)

    def perform_create(self, serializer):

        payment_type=self.request.query_params.get('payment_type')
        
        if payment_type == 'subscription':
            subscription_data = Subscription.objects.get(member=self.request.user)
            serializer.save(member=self.request.user, total_cents=subscription_data.plan.price_cents, metadata={"subscription": str(subscription_data.plan)})
        else:
            serializer.save(member=self.request.user, total_cents=0, metadata={"subscription": "Empty Invoice"})





class PaymentViewSet(BaseModelViewSet):
    #    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrSelf]
    
    def perform_create(self, serializer):
        invoice = Invoice.objects.get(id=self.request.data.get('invoice'))
        if invoice.status == 'PAID':
            return error_response('Invoice already paid', status_code=status.HTTP_400_BAD_REQUEST)
        if invoice.total_cents > self.request.data.get('amount_cents'):
            return error_response('Amount is less than invoice total', status_code=status.HTTP_400_BAD_REQUEST)
        if invoice.total_cents < self.request.data.get('amount_cents'):
            return error_response('Amount is more than invoice total', status_code=status.HTTP_400_BAD_REQUEST)

        if invoice.total_cents <=0:
            return error_response('Invoice total is less than or equal to 0', status_code=status.HTTP_400_BAD_REQUEST)

        if invoice.total_cents == self.request.data.get('amount_cents'):
            invoice.status = 'PAID'
            invoice.save()
            serializer.save(member=self.request.user,amount_cents=invoice.total_cents,status='PAID',reference=str(uuid.uuid4()),paid_at=timezone.now(),metadata={"invoice": str(invoice.number)})
        else:
            serializer.save(member=self.request.user,amount_cents=invoice.total_cents,status='FAILED',reference=str(uuid.uuid4()),paid_at=timezone.now(),metadata={"invoice": str(invoice.number),"subscription": str(invoice.metadata.get('subscription'))})
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN or self.request.user.role == User.STAFF:
            return Payment.objects.all()
        return Payment.objects.filter(member=self.request.user)