"""
Audit log models for immutable system tracking.
"""

import uuid

from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """
    Immutable audit log for tracking all critical system actions.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    claim = models.ForeignKey(
        "claims.Claim",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="audit_actions",
    )

    action = models.CharField(
        max_length=100,
    )

    old_value = models.JSONField(
        null=True,
        blank=True,
    )

    new_value = models.JSONField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        null=True,
        blank=True,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "audit_logs"
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        """
        String representation of audit log.
        """
        return f"{self.action} - {self.timestamp}"

    def save(self, *args, **kwargs):
        """
        Prevent updates to existing audit logs.
        """
        if self.pk and AuditLog.objects.filter(pk=self.pk).exists():
            raise ValueError(
                "Audit logs are immutable and cannot be updated."
            )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Prevent deletion of audit logs.
        """
        raise ValueError(
            "Audit logs are immutable and cannot be deleted."
        )