from rest_framework.routers import DefaultRouter
from django.urls import path, include
from plans.views import MembershipPlanViewSet
from subscriptions.views import SubscriptionViewSet
from payments.views import InvoiceViewSet, PaymentViewSet
from classes.views import FitnessClassViewSet, BookingViewSet, AttendanceViewSet
from feedback.views import FeedbackViewSet
# from reports.views import MembershipReportViewSet, AttendanceReportViewSet, FeedbackReportViewSet, PaymentReportViewSet
from users.views import UserViewSet
router = DefaultRouter()

router.register("membership-plans", MembershipPlanViewSet,basename="membership-plan")
router.register("subscriptions", SubscriptionViewSet,basename="subscription")
router.register("invoices", InvoiceViewSet,basename="invoice")
router.register("payments", PaymentViewSet,basename="payment")
router.register("fitness-classes", FitnessClassViewSet,basename="fitness-class")
router.register("bookings", BookingViewSet,basename="booking")
router.register("attendances", AttendanceViewSet,basename="attendance")
router.register("feedbacks", FeedbackViewSet,basename="feedback")
# router.register("membership-reports", MembershipReportViewSet,basename="membership-report")
# router.register("attendance-reports", AttendanceReportViewSet,basename="attendance-report")
# router.register("feedback-reports", FeedbackReportViewSet,basename="feedback-report")
# router.register("payment-reports", PaymentReportViewSet,basename="payment-report")


# staff endpoints
router.register("user-list", UserViewSet,basename="user-list")

urlpatterns=router.urls
urlpatterns += [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')), 
    path('classes/', include('classes.urls')),
    path('reports/', include('reports.urls')),
]


