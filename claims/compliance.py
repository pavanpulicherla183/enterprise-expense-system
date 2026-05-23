"""
Compliance analysis utilities for expense claims.
"""

from claims.models import EvidenceReuseFlag


class ClaimComplianceAnalyzer:
    """
    Analyze claims for potential transparency
    and compliance concerns.
    """

    @staticmethod
    def analyze(claim):
        """
        Perform lightweight compliance analysis.

        Returns:
            dict:
                Compliance analysis result.
        """

        concerns = []

        evidence_count = (
            claim.evidence_files.count()
        )

        # Missing evidence
        if evidence_count == 0:
            concerns.append(
                "Claim has no supporting evidence."
            )

        # High amount claim
        if claim.amount > 1000:
            concerns.append(
                "High-value claim requires additional review."
            )

        # Excessive evidence uploads
        if evidence_count > 10:
            concerns.append(
                "Large number of evidence files uploaded."
            )

        # Duplicate evidence detected
        duplicate_flag_exists = (
            EvidenceReuseFlag.objects.filter(
                secondary_claim=claim
            ).exists()
        )

        if duplicate_flag_exists:
            concerns.append(
                "Duplicate evidence usage detected."
            )

        # Suspicious file types
        suspicious_files = (
            claim.evidence_files.filter(
                mime_type__in=[
                    "application/x-msdownload",
                    "application/octet-stream",
                ]
            ).exists()
        )

        if suspicious_files:
            concerns.append(
                "Suspicious file type detected."
            )

        return {
            "is_transparent": (
                len(concerns) == 0
            ),
            "concerns": concerns,
        }