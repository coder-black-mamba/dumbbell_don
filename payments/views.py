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

class InvoiceViewSet(BaseModelViewSet):
    # queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminOrSelf]
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN:
            return Invoice.objects.all()
        return Invoice.objects.filter(member=self.request.user)

    def perform_create(self, serializer):

        # payment_type=self.request.query_params.get('subscription')
        
        # if payment_type == 'subscription':
        # else:
        #     return error_response('Please provide payment type', status_code=status.HTTP_400_BAD_REQUEST)
        subscription_data = Subscription.objects.get(member=self.request.user)
        serializer.save(member=self.request.user, total_cents=subscription_data.plan.price_cents, metadata={"subscription": str(subscription_data.plan)})





class PaymentViewSet(BaseModelViewSet):
    #    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrSelf]
    
    def perform_create(self, serializer):
        invoice = Invoice.objects.get(id=self.request.data.get('invoice'))
        print("invoice",invoice)
        invoice.status = 'PAID'
        invoice.save()
        serializer.save(member=self.request.user,amount_cents=invoice.total_cents,status='PAID',reference=str(uuid.uuid4()),metadata={"invoice": str(invoice.number)})
    
    def get_queryset(self):
        if self.request.user.role == User.ADMIN or self.request.user.role == User.STAFF:
            return Payment.objects.all()
        return Payment.objects.filter(member=self.request.user)