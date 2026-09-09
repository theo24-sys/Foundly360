from rest_framework.permissions import BasePermission
from .models import Membership


class OrganizationAccessPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return Membership.objects.filter(user=request.user, organization_id=view.kwargs.get("organization_id"), is_active=True).exists()

    def has_object_permission(self, request, view, obj):
        organization = getattr(obj, "organization", None)
        return bool(organization and Membership.objects.filter(user=request.user, organization=organization, is_active=True).exists())
