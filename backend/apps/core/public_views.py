from rest_framework import generics, permissions
from .models import FoundItem, LostReport, Organization
from .public_serializers import PublicFoundItemSerializer, PublicLostReportSerializer, PublicOrganizationSerializer


class PublicOrganizationListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicOrganizationSerializer
    queryset = Organization.objects.prefetch_related("locations").order_by("name")


class PublicLostReportCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicLostReportSerializer
    queryset = LostReport.objects.all()


class PublicFoundItemCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicFoundItemSerializer
    queryset = FoundItem.objects.all()
