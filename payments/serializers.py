from rest_framework import serializers
from .models import Invoice, Payment

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'member', 'number', 'issue_date', 'due_date', 'total_cents', 'currency', 'status', 'notes', 'metadata']
        read_only_fields = ['id', 'member', 'number', 'issue_date', 'due_date', 'total_cents', 'currency', 'status']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.is_staff:  # admin user
            # allow updating all fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        else:
            # only allow updating non-read-only fields (e.g., notes)
            for attr, value in validated_data.items():
                if attr not in self.Meta.read_only_fields:
                    setattr(instance, attr, value)
        instance.save()
        return instance


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'member', 'amount_cents', 'currency', 'status', 'reference', 'metadata', 'paid_at', 'created_at']
        read_only_fields = ['id', 'member', 'amount_cents', 'currency', 'status', 'reference', 'metadata', 'paid_at', 'created_at']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.is_staff:  # admin user
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        else:
            for attr, value in validated_data.items():
                if attr not in self.Meta.read_only_fields:
                    setattr(instance, attr, value)
        instance.save()
        return instance
