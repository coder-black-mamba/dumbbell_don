from django.http import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from core.utils.api_response import success_response,error_response
from rest_framework.permissions import IsAdminUser
from payments.models import Invoice
from django.db.models import Sum,Count,Avg
from classes.models import Attendance
from classes.serializers import MemberAttendanceSerializer
from feedback.models import Feedback
from subscriptions.models import Subscription
from reports.serializers import FeedbackReportSerializer,SubscriptionReportSerializer

# membership documentation done [wrong commit on commit 9d662846a1897253b2b1b134cd715dbbbd217dee]
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
@permission_classes([IsAdminUser])
def get_attendance_report(request): 
    class_id=request.query_params.get('class_id')
    if not class_id:
        return error_response(message="Class ID is required")
    
    attendance=Attendance.objects.select_related('booking__member').filter(booking__fitness_class_id=class_id)
    participant_count=attendance.values('booking__member').distinct().count() 
    
    preset_students=attendance.filter(present=True).count()
    absent_students=attendance.filter(present=False).count()
    present_percentage=preset_students/attendance.count()
    absent_percentage=absent_students/attendance.count()

    serializer=MemberAttendanceSerializer(attendance, many=True)
    stats={"total_attendance":attendance.count(),"total_members":participant_count,"absent":absent_students,"present":preset_students,"present_percentage":present_percentage*100,"absent_percentage":absent_percentage*100}
    return success_response(data={"stats":stats,"report":serializer.data})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_feedback_report(request):
    feedback=Feedback.objects.all()


    stats={"total_feedback":feedback.count(),"total_members":feedback.values('member').distinct().count(),"total_positive":feedback.filter(rating__gte=4).count(),"total_negative":feedback.filter(rating__lte=2).count() ,"total_neutral":feedback.filter(rating__gte=2,rating__lte=4).count(),"average_rating":feedback.aggregate(avg=Avg('rating'))['avg'],"rating_distribution":feedback.values('rating').annotate(count=Count('rating')),}
    
    
    
    
    serializer=FeedbackReportSerializer(feedback, many=True)
    return success_response(data={"stats":stats,"report":serializer.data})



@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_membership_report(request):
    subscriptions=Subscription.objects.all()
    serializer= SubscriptionReportSerializer(subscriptions, many=True)

    stats={"total_subscriptions":subscriptions.count(),"total_members":subscriptions.values('member').distinct().count(),"total_active":subscriptions.filter(status='ACTIVE').count(),"total_inactive":subscriptions.filter(status='INACTIVE').count(),"total_cancelled":subscriptions.filter(status='CANCELLED').count(),"total_expiring":subscriptions.filter(status='EXPIRING').count(),"total_expired":subscriptions.filter(status='EXPIRED').count(),"total_auto_renew":subscriptions.filter(auto_renew=True).count(),}
    
    
    return success_response(data={"stats":stats,"report":serializer.data})