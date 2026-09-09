from django.db.models import Count
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Claim, FoundItem, Location, LostReport, MatchSuggestion, Organization, StorageBin
from .permissions import OrganizationAccessPermission
from .serializers import ClaimSerializer, FoundItemSerializer, LocationSerializer, LostReportSerializer, MatchSuggestionSerializer, StorageBinSerializer


class ScopedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [OrganizationAccessPermission]
    organization_model = Organization

    def get_organization(self):
        return Organization.objects.get(pk=self.kwargs["organization_id"])

    def get_queryset(self):
        return self.queryset.filter(organization_id=self.kwargs["organization_id"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["organization"] = self.get_organization()
        return context


class LocationViewSet(ScopedModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class StorageBinViewSet(ScopedModelViewSet):
    queryset = StorageBin.objects.all()
    serializer_class = StorageBinSerializer


class FoundItemViewSet(ScopedModelViewSet):
    queryset = FoundItem.objects.select_related("location", "storage_bin").all()
    serializer_class = FoundItemSerializer
    filterset_fields = ["status", "category", "restricted"]


class LostReportViewSet(ScopedModelViewSet):
    queryset = LostReport.objects.all()
    serializer_class = LostReportSerializer
    filterset_fields = ["status", "category"]


class MatchSuggestionViewSet(ScopedModelViewSet):
    queryset = MatchSuggestion.objects.select_related("found_item", "lost_report").all()
    serializer_class = MatchSuggestionSerializer


class ClaimViewSet(ScopedModelViewSet):
    queryset = Claim.objects.select_related("found_item").all()
    serializer_class = ClaimSerializer
    filterset_fields = ["status"]


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def dashboard(request, organization_id):
    allowed = OrganizationAccessPermission().has_permission(request, type("View", (), {"kwargs": {"organization_id": organization_id}})())
    if not allowed:
        return Response({"detail": "You do not have access to this organization."}, status=403)
    items = FoundItem.objects.filter(organization_id=organization_id)
    return Response({
        "open_cases": items.exclude(status__in=[FoundItem.Status.RETURNED, FoundItem.Status.DISPOSED]).count(),
        "possible_matches": items.filter(status=FoundItem.Status.MATCHED).count(),
        "pending_claims": Claim.objects.filter(organization_id=organization_id, status=Claim.Status.SUBMITTED).count(),
        "recovery_rate": 0,
        "category_breakdown": list(items.values("category").annotate(total=Count("id")).order_by("-total")),
    })
