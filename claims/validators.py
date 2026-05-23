"""
Evidence validation rules for claim approval.
"""

from rest_framework.exceptions import ValidationError


class EvidenceValidator:
    """
    Validate evidence sufficiency requirements.
    """

    @staticmethod
    def validate_for_approval(claim):
        """
        Validate whether claim contains sufficient
        evidence for approval workflow.

        Raises:
            ValidationError:
                If evidence requirements are not met.
        """

        evidence_files = (
            claim.evidence_files.all()
        )

        if not evidence_files.exists():
            raise ValidationError({
                "detail":
                    "Claim cannot be approved "
                    "without evidence."
            })

        # High-value claim validation
        if claim.amount > 100:

            valid_keywords = [
                "receipt",
                "invoice",
            ]

            has_required_document = any(
                any(
                    keyword in evidence.file_name.lower()
                    for keyword in valid_keywords
                )
                for evidence in evidence_files
            )

            if not has_required_document:
                raise ValidationError({
                    "detail":
                        "Claims above $100 require "
                        "a receipt or invoice."
                })