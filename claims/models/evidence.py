"""
Evidence models for claim document management.
"""

import hashlib
import uuid

from django.conf import settings
from django.db import models


def evidence_upload_path(instance, filename):
    """
    Generate upload path for evidence files.
    """
    return f"claims/{instance.claim.id}/evidence/{filename}"


class Evidence(models.Model):
    """
    Immutable evidence attachment for expense claims.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    claim = models.ForeignKey(
        "claims.Claim",
        on_delete=models.CASCADE,
        related_name="evidence_files",
    )

    file = models.FileField(
        upload_to=evidence_upload_path,
    )

    file_name = models.CharField(
        max_length=255,
    )

    file_size = models.PositiveIntegerField()

    mime_type = models.CharField(
        max_length=100,
    )

    content_hash = models.CharField(
        max_length=64,
        db_index=True,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_evidence",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "evidence"
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        """
        String representation of evidence.
        """
        return self.file_name

    def save(self, *args, **kwargs):
        """
        Automatically generate SHA256 hash before saving.
        """
        if self.file and not self.content_hash:
            sha256 = hashlib.sha256()

            for chunk in self.file.chunks():
                sha256.update(chunk)

            self.content_hash = sha256.hexdigest()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Prevent deletion of immutable evidence after upload.
        """
        raise ValueError(
            "Evidence records are immutable and cannot be deleted."
        )