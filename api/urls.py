from rest_framework.routers import DefaultRouter
from django.urls import path, include
from plans.views import MembershipPlanViewSet
from subscriptions.views import SubscriptionViewSet

router = DefaultRouter()
router.register("membership-plans", MembershipPlanViewSet,basename="membership-plan")
router.register("subscriptions", SubscriptionViewSet,basename="subscription")



urlpatterns=router.urls
urlpatterns += [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
