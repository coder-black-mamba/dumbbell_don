from django.urls import path
from .views import get_membership_report,get_attendance_report,get_feedback_report,get_payment_report

urlpatterns = [
    path('membership-reports/', get_membership_report  ,name="membership-report"),
    path('attendance-reports/', get_attendance_report,name="attendance-report"),
    path('feedback-reports/', get_feedback_report,name="feedback-report"),
    path('payment-reports/', get_payment_report,name="payment-report"),
]