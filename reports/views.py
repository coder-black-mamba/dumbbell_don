from django.http import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from core.utils.api_response import success_response,error_response
from rest_framework.permissions import IsAdminUser
from payments.models import Invoice
from django.db.models import Sum
from classes.models import Attendance
from classes.serializers import MemberAttendanceSerializer
from feedback.models import Feedback
from users.models import User
from subscriptions.models import Subscription

@permission_classes([IsAdminUser])
@api_view(['GET'])
def get_payment_report(request):
    # for stats and report fields took help from ai 
    invoices = Invoice.objects.all().select_related('member').prefetch_related('payments')
    report = []
    for invoice in invoices:
        total_paid_cents = invoice.payments.filter(status='PAID').aggregate(
            total=Sum('amount_cents')
        )['total'] or 0

        outstanding_cents = invoice.total_cents - total_paid_cents

        # Determine status
        if total_paid_cents >= invoice.total_cents:
            report_status = 'PAID'
        elif total_paid_cents == 0:
            report_status = 'UNPAID'
        else:
            report_status = 'PARTIAL'

        report.append({
            "invoice_number": invoice.number,
            "member_email": invoice.member.email,
            "invoice_total": f"${invoice.total_cents / 100:.2f}",
            "total_paid": f"${total_paid_cents / 100:.2f}",
            "outstanding_balance": f"${outstanding_cents / 100:.2f}",
            "status": report_status,
            "payments": [
                {
                    "reference": p.reference,
                    "amount": f"${p.amount_cents / 100:.2f}",
                    "currency": p.currency,
                    "status": p.status,
                    "paid_at": p.paid_at
                }
                for p in invoice.payments.all()
            ]
        })


    # lets aggregate it first 
    total_paid = sum(invoice.payments.filter(status='PAID').aggregate(total=Sum('amount_cents'))['total'] or 0 for invoice in invoices)

    total_outstanding = sum(invoice.total_cents for invoice in invoices) - total_paid
    total_invoices = invoices.count()
    total_payments = sum(invoice.payments.count() for invoice in invoices)
    return success_response(data={"stats":{"total_paid":f"${total_paid/100}","total_outstanding":f"${total_outstanding/100}","total_invoices":total_invoices,"total_payments":total_payments},"report":report})



@api_view(['GET'])
def get_attendance_report(request): 
    return HttpResponse("Attendance Report")


@api_view(['GET'])
def get_feedback_report(request):
    return HttpResponse("Feedback Report")



@api_view(['GET'])
def get_membership_report(request):
    return HttpResponse("Membership Report")


@api_view(['GET'])
def get_subscription_report(request):
    return HttpResponse("Subscription Report")