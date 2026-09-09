from rest_framework import serializers
from .models import Claim, FoundItem, Location, LostReport, MatchSuggestion, StorageBin


class OrganizationScopedSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        validated_data["organization"] = self.context["organization"]
        return super().create(validated_data)


class LocationSerializer(OrganizationScopedSerializer):
    class Meta:
        model = Location
        fields = ["id", "organization", "name", "address", "is_active"]


class StorageBinSerializer(OrganizationScopedSerializer):
    class Meta:
        model = StorageBin
        fields = ["id", "organization", "code", "label", "is_active"]


class FoundItemSerializer(OrganizationScopedSerializer):
    class Meta:
        model = FoundItem
        fields = ["id", "organization", "reference", "category", "title", "private_description", "status", "restricted", "found_at", "location", "storage_bin", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        organization = self.context["organization"]
        for field in ("location", "storage_bin"):
            obj = attrs.get(field)
            if obj and obj.organization_id != organization.id:
                raise serializers.ValidationError({field: "Must belong to the active organization."})
        return attrs


class LostReportSerializer(OrganizationScopedSerializer):
    class Meta:
        model = LostReport
        fields = ["id", "organization", "reference", "claimant_name", "claimant_phone", "category", "description", "last_seen_location", "lost_at", "status", "created_at"]
        read_only_fields = ["created_at", "status"]


class MatchSuggestionSerializer(OrganizationScopedSerializer):
    class Meta:
        model = MatchSuggestion
        fields = ["id", "organization", "found_item", "lost_report", "score", "signals", "status", "created_at"]
        read_only_fields = ["created_at"]


class ClaimSerializer(OrganizationScopedSerializer):
    class Meta:
        model = Claim
        fields = ["id", "organization", "found_item", "claimant_name", "claimant_phone", "evidence", "status", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at", "status"]

    def validate_found_item(self, value):
        if value.organization_id != self.context["organization"].id:
            raise serializers.ValidationError("Item must belong to the active organization.")
        return value
