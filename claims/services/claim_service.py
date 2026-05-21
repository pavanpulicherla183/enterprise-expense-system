"""
Business logic services for claim workflows.
"""

from django.db import transaction
from claims.models import AuditLog, Claim, ClaimStatus, ClaimStatusHistory, Evidence
from rest_framework.exceptions import PermissionDenied, ValidationError
from claims.models import EvidenceReuseFlag

class ClaimService:
    """
    Service layer for claim-related workflows.
    """

    @staticmethod
    @transaction.atomic
    def create_claim(*, employee, validated_data):
        """
        Create a new expense claim with audit logging.
        """

        claim = Claim.objects.create(
            employee=employee,
            **validated_data,
        )

        AuditLog.objects.create(
            claim=claim,
            actor=employee,
            action="CLAIM_CREATED",
            old_value=None,
            new_value={
                "claim_id": claim.id,
                "status": claim.status,
                "amount": str(claim.amount),
                "description": claim.description,
            },
        )

        return claim
    
    @staticmethod
    @transaction.atomic
    def submit_claim(*, claim, employee):
        """
        Submit claim into review workflow.
        """

        if claim.employee != employee:
            raise PermissionDenied(
                "You can only submit your own claims."
            )

        allowed_states = [
            ClaimStatus.DRAFT,
            ClaimStatus.CHANGES_REQUESTED,
        ]

        if claim.status not in allowed_states:
            raise ValidationError(
                "Claim cannot be submitted from current state."
            )

        if not claim.evidence_files.exists():
            raise ValidationError(
                "At least one evidence file is required."
            )

        old_status = claim.status

        new_status = (
            ClaimStatus.SUBMITTED
            if claim.status == ClaimStatus.DRAFT
            else ClaimStatus.RESUBMITTED
        )

        claim.status = new_status
        claim.version += 1
        claim.save()

        ClaimStatusHistory.objects.create(
            claim=claim,
            old_status=old_status,
            new_status=new_status,
            changed_by=employee,
        )

        AuditLog.objects.create(
            claim=claim,
            actor=employee,
            action="CLAIM_SUBMITTED",
            old_value={
                "status": old_status,
            },
            new_value={
                "status": new_status,
            },
        )

        return claim

    @staticmethod
    @transaction.atomic
    def upload_evidence(*, claim, uploaded_by, uploaded_file):
        """
        Upload evidence for a claim.
        """

        if claim.employee != uploaded_by:
            raise PermissionDenied(
                "You can only upload evidence to your own claims."
            )

        evidence = Evidence.objects.create(
            claim=claim,
            file=uploaded_file,
            file_name=uploaded_file.name,
            file_size=uploaded_file.size,
            mime_type=uploaded_file.content_type,
            uploaded_by=uploaded_by,
        )

        duplicate_evidence = (
            Evidence.objects.filter(
                content_hash=evidence.content_hash,
            )
            .exclude(id=evidence.id)
            .first()
        )

        if duplicate_evidence:
            EvidenceReuseFlag.objects.create(
                evidence=evidence,
                primary_claim=duplicate_evidence.claim,
                secondary_claim=claim,
                flagged_by=uploaded_by,
            )

            AuditLog.objects.create(
                claim=claim,
                actor=uploaded_by,
                action="DUPLICATE_EVIDENCE_DETECTED",
                old_value=None,
                new_value={
                    "original_evidence_id": str(
                        duplicate_evidence.id
                    ),
                    "duplicate_evidence_id": str(
                        evidence.id
                    ),
                    "content_hash": evidence.content_hash,
                },
            )

        AuditLog.objects.create(
            claim=claim,
            actor=uploaded_by,
            action="EVIDENCE_UPLOADED",
            old_value=None,
            new_value={
                "evidence_id": str(evidence.id),
                "file_name": evidence.file_name,
                "content_hash": evidence.content_hash,
            },
        )

        return evidence
    
    @staticmethod
    @transaction.atomic
    def review_claim(
        *,
        claim,
        reviewer,
        target_status,
        action,
    ):
        """
        Handle reviewer workflow transitions.
        """

        allowed_states = [
            ClaimStatus.SUBMITTED,
            ClaimStatus.RESUBMITTED,
        ]

        if claim.status not in allowed_states:
            raise ValidationError(
                "Claim is not available for review."
            )

        old_status = claim.status

        claim.status = target_status
        claim.version += 1
        claim.save()

        ClaimStatusHistory.objects.create(
            claim=claim,
            old_status=old_status,
            new_status=target_status,
            changed_by=reviewer,
        )

        AuditLog.objects.create(
            claim=claim,
            actor=reviewer,
            action=action,
            old_value={
                "status": old_status,
            },
            new_value={
                "status": target_status,
            },
        )

        return claim

    @staticmethod
    @transaction.atomic
    def finalize_claim(*, claim, controller):
        """
        Finalize approved claim.
        """

        if claim.status != ClaimStatus.APPROVED:
            raise ValidationError(
                "Only approved claims can be finalized."
            )

        old_status = claim.status

        claim.status = ClaimStatus.FINALIZED
        claim.version += 1
        claim.save()

        ClaimStatusHistory.objects.create(
            claim=claim,
            old_status=old_status,
            new_status=ClaimStatus.FINALIZED,
            changed_by=controller,
        )

        AuditLog.objects.create(
            claim=claim,
            actor=controller,
            action="CLAIM_FINALIZED",
            old_value={
                "status": old_status,
            },
            new_value={
                "status": ClaimStatus.FINALIZED,
            },
        )

        return claim