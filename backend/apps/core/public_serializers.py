from django.utils import timezone
from rest_framework import serializers
from .models import FoundItem, Location, LostReport, Organization


class PublicLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name", "kind", "address", "opening_hours", "contact_phone"]


class PublicOrganizationSerializer(serializers.ModelSerializer):
    receiving_points = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ["id", "name", "slug", "receiving_points"]

    def get_receiving_points(self, organization):
        locations = organization.locations.filter(is_active=True, is_receiving_point=True)
        return PublicLocationSerializer(locations, many=True).data


class PublicLostReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostReport
        fields = ["organization", "claimant_name", "claimant_phone", "category", "description", "last_seen_location", "lost_at"]
        extra_kwargs = {"lost_at": {"required": False}}

    def create(self, validated_data):
        organization = validated_data["organization"]
        reference = self._reference(organization)
        validated_data.setdefault("lost_at", timezone.now())
        return LostReport.objects.create(reference=reference, **validated_data)

    @staticmethod
    def _reference(organization):
        prefix = f"LR-{timezone.now():%Y%m%d}"
        count = LostReport.objects.filter(organization=organization, reference__startswith=prefix).count() + 1
        return f"{prefix}-{count:04d}"


class PublicFoundItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoundItem
        fields = ["organization", "location", "category", "title", "private_description", "found_at"]
        extra_kwargs = {"found_at": {"required": False}}

    def validate(self, attrs):
        location = attrs["location"]
        organization = attrs["organization"]
        if location.organization_id != organization.id or not location.is_active or not location.is_receiving_point:
            raise serializers.ValidationError({"location": "Choose an active receiving point for this institution."})
        return attrs

    def create(self, validated_data):
        organization = validated_data["organization"]
        prefix = f"LP-{timezone.now():%Y%m%d}"
        count = FoundItem.objects.filter(organization=organization, reference__startswith=prefix).count() + 1
        validated_data.setdefault("found_at", timezone.now())
        return FoundItem.objects.create(reference=f"{prefix}-{count:04d}", **validated_data)
