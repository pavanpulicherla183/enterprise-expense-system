"""
Claim model definitions for the expense workflow system.
"""

from django.conf import settings
from django.db import models


class ClaimStatus(models.TextChoices):
    """
    Enumeration for supported claim states.
    """

    DRAFT = "DRAFT", "Draft"
    SUBMITTED = "SUBMITTED", "Submitted"
    CHANGES_REQUESTED = "CHANGES_REQUESTED", "Changes Requested"
    RESUBMITTED = "RESUBMITTED", "Resubmitted"
    APPROVED = "APPROVED", "Approved"
    FINALIZED = "FINALIZED", "Finalized"
    REJECTED = "REJECTED", "Rejected"


class Claim(models.Model):
    """
    Represents an employee expense claim.
    """

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="claims",
    )

    status = models.CharField(
        max_length=30,
        choices=ClaimStatus.choices,
        default=ClaimStatus.DRAFT,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    description = models.TextField()

    purpose = models.TextField()

    finalized_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    version = models.PositiveIntegerField(
        default=1,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "claims"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["employee"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self) -> str:
        """
        String representation of claim.
        """
        return f"Claim #{self.id} - {self.status}"