"""
Selectors for claim retrieval queries.
"""

from claims.models import Claim, UserRole


def get_claim_by_id(*, claim_id):
    """
    Retrieve claim by ID.
    """

    return Claim.objects.get(
        id=claim_id,
    )


def get_claims_for_user(*, user):
    """
    Retrieve claims visible to current user.
    """

    if user.role == UserRole.EMPLOYEE:
        return Claim.objects.filter(
            employee=user,
        ).order_by("-created_at")

    return Claim.objects.all().order_by(
        "-created_at"
    )