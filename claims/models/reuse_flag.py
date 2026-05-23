"""
Evidence reuse tracking models.
"""

from django.conf import settings
from django.db import models


class EvidenceReuseFlag(models.Model):
    """
    Tracks evidence reuse across multiple claims.
    """

    evidence = models.ForeignKey(
        "claims.Evidence",
        on_delete=models.CASCADE,
        related_name="reuse_flags",
    )

    primary_claim = models.ForeignKey(
        "claims.Claim",
        on_delete=models.CASCADE,
        related_name="primary_reuse_flags",
    )

    secondary_claim = models.ForeignKey(
        "claims.Claim",
        on_delete=models.CASCADE,
        related_name="secondary_reuse_flags",
    )

    flagged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="flagged_reuse_cases",
    )

    reviewer_notes = models.TextField(
        null=True,
        blank=True,
    )

    resolved = models.BooleanField(
        default=False,
    )

    resolution_notes = models.TextField(
        null=True,
        blank=True,
    )

    flagged_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "evidence_reuse_flags"
        ordering = ["-flagged_at"]
        indexes = [
            models.Index(fields=["evidence"]),
            models.Index(fields=["primary_claim"]),
            models.Index(fields=["secondary_claim"]),
            models.Index(fields=["flagged_at"]),
        ]

    def __str__(self) -> str:
        """
        String representation of reuse flag.
        """
        return (
            f"Evidence reuse detected "
            f"between Claim #{self.primary_claim_id} "
            f"and Claim #{self.secondary_claim_id}"
        )