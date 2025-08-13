from rest_framework import serializers
from .models import Invoice, Payment

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'member', 'number', 'issue_date', 'due_date', 'total_cents', 'currency', 'status', 'notes', 'metadata']
        read_only_fields = ['id', 'member', 'number', 'issue_date', 'due_date', 'total_cents', 'currency','status']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'member', 'amount_cents', 'currency', 'status', 'reference', 'metadata', 'paid_at', 'created_at']
        read_only_fields = ['id', 'member', 'amount_cents', 'currency', 'status', 'reference', 'metadata', 'paid_at', 'created_at']