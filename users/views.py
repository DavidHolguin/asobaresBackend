# users/views.py

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import UserProfile, DigitalCard
from .serializers import UserProfileSerializer, DigitalCardSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.userprofile.is_admin:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

class DigitalCardViewSet(viewsets.ModelViewSet):
    queryset = DigitalCard.objects.all()
    serializer_class = DigitalCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.userprofile.is_admin:
            return DigitalCard.objects.all()
        return DigitalCard.objects.filter(user_profile__user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verify_card(request, card_id):
    try:
        card = DigitalCard.objects.get(card_id=card_id)
        if not card.is_active:
            return Response(
                {"detail": "Card is inactive"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = DigitalCardSerializer(card)
        return Response(serializer.data)
    except DigitalCard.DoesNotExist:
        return Response(
            {"detail": "Card not found"},
            status=status.HTTP_404_NOT_FOUND
        )

