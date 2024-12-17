from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from ad.models import Advertisement
from ad.permissions import IsAuthorOrAdmin
from ad.serializers import AdvertisementSummarySerializer, AdvertisementSerializer


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthorOrAdmin]

    def get_serializer_class(self):
        if self.action == 'list':
            return AdvertisementSummarySerializer
        return AdvertisementSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [AllowAny()]
        return [IsAuthorOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)