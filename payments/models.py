from django.db import models
from django.utils import timezone
from users.models import User
from datetime import timedelta

def generate_invoice_number():
    return f"INV-{timezone.now().strftime('%Y%m%d%H%M%S')}"

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    )

    member = models.ForeignKey('users.User', on_delete=models.CASCADE)
    number = models.CharField(max_length=50, unique=True, default=generate_invoice_number)   
    issue_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(default=timezone.localdate() + timedelta(days=7))
    total_cents = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    notes = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Invoice {self.number} - {self.member.email}"


class Payment(models.Model):
    STATUS_CHOICES = (
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending')
    )

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    member = models.ForeignKey('users.User', on_delete=models.CASCADE)
    amount_cents = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    reference = models.CharField(max_length=255, unique=True)  # Payment gateway ref
    metadata = models.JSONField(default=dict, blank=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_paid(self):
        """Mark this payment as paid and update invoice if fully paid."""
        self.status = 'PAID'
        self.paid_at = timezone.now()
        self.save()

        # Update invoice status if fully paid
        total_paid = sum(p.amount_cents for p in self.invoice.payments.filter(status='PAID'))
        if total_paid >= self.invoice.total_cents:
            self.invoice.status = 'PAID'
            self.invoice.save()

    def __str__(self):
        return f"Payment {self.reference} - {self.get_status_display()}"
