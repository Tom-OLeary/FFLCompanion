from django.db import models
from django.utils import timezone

from owner.models import Owner


class NotificationManager(models.Manager):
    def submit(self, title: str, message: str, notification_type: str, owner: Owner = None):
        self.create(
            title=title,
            message=message,
            notification_type=notification_type,
            owner=owner,
        )


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        ALERT = "alert"  # app-wide alert regardless of user
        USER = "user"

    class Meta:
        db_table = 'notifications'

    title = models.CharField(max_length=255, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    notification_type = models.CharField(max_length=255, null=False, blank=False, choices=NotificationType.choices)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
    expires_at = models.DateTimeField(null=False, blank=False, default=timezone.now)

    objects = NotificationManager()
