from rest_framework.routers import DefaultRouter
from django.urls import path, include
from plans.views import MembershipPlanViewSet
from subscriptions.views import SubscriptionViewSet
from payments.views import InvoiceViewSet, PaymentViewSet
from classes.views import FitnessClassViewSet, BookingViewSet, AttendanceViewSet

router = DefaultRouter()

router.register("membership-plans", MembershipPlanViewSet,basename="membership-plan")
router.register("subscriptions", SubscriptionViewSet,basename="subscription")
router.register("invoices", InvoiceViewSet,basename="invoice")
router.register("payments", PaymentViewSet,basename="payment")
router.register("fitness-classes", FitnessClassViewSet,basename="fitness-class")
router.register("bookings", BookingViewSet,basename="booking")
router.register("attendances", AttendanceViewSet,basename="attendance")

urlpatterns=router.urls
urlpatterns += [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
