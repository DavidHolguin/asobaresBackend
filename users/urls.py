# users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, DigitalCardViewSet, verify_card

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'cards', DigitalCardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verify-card/<uuid:card_id>/', verify_card, name='verify-card'),
]