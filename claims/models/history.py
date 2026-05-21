"""
Claim status history models.
"""

from django.conf import settings
from django.db import models

from claims.models.claim import ClaimStatus


class ClaimStatusHistory(models.Model):
    """
    Stores immutable claim status transition history.
    """

    claim = models.ForeignKey(
        "claims.Claim",
        on_delete=models.CASCADE,
        related_name="status_history",
    )

    old_status = models.CharField(
        max_length=30,
        choices=ClaimStatus.choices,
    )

    new_status = models.CharField(
        max_length=30,
        choices=ClaimStatus.choices,
    )

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="claim_status_changes",
    )

    reason = models.TextField(
        null=True,
        blank=True,
    )

    changed_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "claim_status_history"
        ordering = ["-changed_at"]

    def __str__(self) -> str:
        """
        String representation of claim history.
        """
        return (
            f"Claim #{self.claim_id}: "
            f"{self.old_status} → {self.new_status}"
        )