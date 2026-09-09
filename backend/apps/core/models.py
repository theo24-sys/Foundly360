from django.conf import settings
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    class Role(models.TextChoices):
        ORG_ADMIN = "ORG_ADMIN", "Organization admin"
        SUPERVISOR = "SUPERVISOR", "Supervisor"
        OFFICER = "OFFICER", "Officer"
        VIEWER = "VIEWER", "Viewer"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organization_memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.OFFICER)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("organization", "user"), name="unique_membership_per_org")]


class Location(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=160)
    address = models.CharField(max_length=240, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("organization", "name"), name="unique_location_per_org")]


class StorageBin(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="storage_bins")
    code = models.CharField(max_length=40)
    label = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("organization", "code"), name="unique_bin_per_org")]


class FoundItem(models.Model):
    class Status(models.TextChoices):
        STORED = "STORED", "Stored"
        MATCHED = "MATCHED", "Matched"
        CLAIM_PENDING = "CLAIM_PENDING", "Claim pending"
        RETURNED = "RETURNED", "Returned"
        DISPOSED = "DISPOSED", "Disposed"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="found_items")
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="found_items")
    storage_bin = models.ForeignKey(StorageBin, on_delete=models.PROTECT, related_name="found_items", null=True, blank=True)
    reference = models.CharField(max_length=32)
    category = models.CharField(max_length=80)
    title = models.CharField(max_length=180)
    private_description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.STORED)
    restricted = models.BooleanField(default=False)
    found_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("organization", "reference"), name="unique_reference_per_org")]
        indexes = [models.Index(fields=("organization", "status")), models.Index(fields=("organization", "category"))]


class CustodyEvent(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="custody_events")
    item = models.ForeignKey(FoundItem, on_delete=models.PROTECT, related_name="custody_events")
    event_type = models.CharField(max_length=60)
    actor_id = models.IntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=("organization", "created_at"))]


class LostReport(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        MATCHED = "MATCHED", "Matched"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="lost_reports")
    reference = models.CharField(max_length=32)
    claimant_name = models.CharField(max_length=180)
    claimant_phone = models.CharField(max_length=40)
    category = models.CharField(max_length=80)
    description = models.TextField()
    last_seen_location = models.CharField(max_length=180)
    lost_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("organization", "reference"), name="unique_lost_reference_per_org")]
        indexes = [models.Index(fields=("organization", "status")), models.Index(fields=("organization", "category"))]


class MatchSuggestion(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="match_suggestions")
    found_item = models.ForeignKey(FoundItem, on_delete=models.PROTECT, related_name="match_suggestions")
    lost_report = models.ForeignKey(LostReport, on_delete=models.PROTECT, related_name="match_suggestions")
    score = models.PositiveSmallIntegerField()
    signals = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("found_item", "lost_report"), name="unique_match_pair")]


class Claim(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        EVIDENCE_REQUIRED = "EVIDENCE_REQUIRED", "Evidence required"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        COLLECTED = "COLLECTED", "Collected"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="claims")
    found_item = models.ForeignKey(FoundItem, on_delete=models.PROTECT, related_name="claims")
    claimant_name = models.CharField(max_length=180)
    claimant_phone = models.CharField(max_length=40)
    evidence = models.TextField()
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.SUBMITTED)
    collection_pin_hash = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transfer(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "REQUESTED", "Requested"
        IN_TRANSIT = "IN_TRANSIT", "In transit"
        RECEIVED = "RECEIVED", "Received"
        CANCELLED = "CANCELLED", "Cancelled"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="transfers")
    found_item = models.ForeignKey(FoundItem, on_delete=models.PROTECT, related_name="transfers")
    from_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="outgoing_transfers")
    to_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="incoming_transfers")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="requested_transfers")
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="received_transfers", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(null=True, blank=True)


class DisposalEvent(models.Model):
    class Method(models.TextChoices):
        AUCTION = "AUCTION", "Auction"
        DONATION = "DONATION", "Donation"
        DESTRUCTION = "DESTRUCTION", "Destruction"
        RETURNED_TO_AUTHORITY = "RETURNED_TO_AUTHORITY", "Returned to authority"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="disposal_events")
    found_item = models.OneToOneField(FoundItem, on_delete=models.PROTECT, related_name="disposal_event")
    method = models.CharField(max_length=32, choices=Method.choices)
    notice_issued_at = models.DateTimeField(null=True, blank=True)
    disposed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="approved_disposals", null=True, blank=True)


class Notification(models.Model):
    class Channel(models.TextChoices):
        SMS = "SMS", "SMS"
        WHATSAPP = "WHATSAPP", "WhatsApp"
        EMAIL = "EMAIL", "Email"

    class Status(models.TextChoices):
        QUEUED = "QUEUED", "Queued"
        SENT = "SENT", "Sent"
        FAILED = "FAILED", "Failed"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="notifications")
    channel = models.CharField(max_length=12, choices=Channel.choices)
    recipient = models.CharField(max_length=180)
    template = models.CharField(max_length=80)
    provider_id = models.CharField(max_length=180, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.QUEUED)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        FAILED = "FAILED", "Failed"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    phone_number = models.CharField(max_length=40)
    checkout_request_id = models.CharField(max_length=180, blank=True)
    receipt_number = models.CharField(max_length=180, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)


class AuditLog(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="audit_logs")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    action = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=80)
    resource_id = models.CharField(max_length=80)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class RetentionJob(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="retention_jobs")
    target_type = models.CharField(max_length=80)
    target_id = models.CharField(max_length=80)
    scheduled_for = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="QUEUED")


class PreventativeTag(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="preventative_tags")
    code = models.CharField(max_length=80)
    owner_phone = models.CharField(max_length=40, blank=True)
    label = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("organization", "code"), name="unique_preventative_tag_per_org")]
