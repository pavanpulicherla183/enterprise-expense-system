from celery import shared_task
from claims.models import Evidence, EvidenceReuseFlag, AuditLog

@shared_task
def detect_duplicate_evidence(evidence_id):
    """
    Detect duplicate evidence asynchronously.

    This task checks whether the uploaded evidence file
    has already been used in another claim based on the
    SHA256 content hash.

    Running this in the background keeps evidence upload
    APIs fast and scalable under high traffic.

    If duplicate evidence is found:
    - A reuse flag is created.
    - An audit log entry is recorded.

    Args:
        evidence_id:
            ID of the uploaded evidence.
    """
    try:
        evidence = Evidence.objects.get(id=evidence_id)

        duplicate = (
            Evidence.objects.filter(
                content_hash=evidence.content_hash
            )
            .exclude(id=evidence.id)
            .first()
        )

        if duplicate:
            EvidenceReuseFlag.objects.create(
                evidence=evidence,
                primary_claim=duplicate.claim,
                secondary_claim=evidence.claim,
                flagged_by=evidence.uploaded_by,
            )

            AuditLog.objects.create(
                claim=evidence.claim,
                actor=evidence.uploaded_by,
                action="DUPLICATE_EVIDENCE_DETECTED",
                old_value=None,
                new_value={
                    "original_evidence_id": str(
                        duplicate.id
                    ),
                    "duplicate_evidence_id": str(
                        evidence.id
                    ),
                    "content_hash": evidence.content_hash,
                },
            )

    except Evidence.DoesNotExist:
        pass