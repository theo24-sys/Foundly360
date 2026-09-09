from celery import shared_task
from django.utils import timezone
from .models import Notification, RetentionJob


@shared_task
def dispatch_notification(notification_id):
    notification = Notification.objects.get(pk=notification_id)
    # Provider adapters will update provider_id and status after credentials are configured.
    notification.status = Notification.Status.FAILED
    notification.payload = {**notification.payload, "error": "Provider adapter not configured"}
    notification.save(update_fields=["status", "payload"])
    return notification_id


@shared_task
def process_retention_jobs():
    jobs = RetentionJob.objects.filter(status="QUEUED", scheduled_for__lte=timezone.now())
    return jobs.update(status="COMPLETED", completed_at=timezone.now())
