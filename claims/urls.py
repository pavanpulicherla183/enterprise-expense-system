"""
URL routing for claim APIs.
"""

from django.urls import path
from claims.views import (
    ClaimCreateAPIView,
    ClaimSubmitAPIView,
    EvidenceUploadAPIView,
    ClaimApproveAPIView,
    ClaimRejectAPIView,
    ClaimRequestChangesAPIView,
    ClaimFinalizeAPIView,
    ClaimDetailAPIView,
)

urlpatterns = [
    path(
        "claims/",
        ClaimCreateAPIView.as_view(),
        name="claim-create",
    ),
    path(
        "claims/<int:claim_id>/submit/",
        ClaimSubmitAPIView.as_view(),
        name="claim-submit",
    ),
    path(
        "claims/<int:claim_id>/evidence/",
        EvidenceUploadAPIView.as_view(),
        name="evidence-upload",
    ),
    path(
        "claims/<int:claim_id>/approve/",
        ClaimApproveAPIView.as_view(),
        name="claim-approve",
    ),
    path(
        "claims/<int:claim_id>/reject/",
        ClaimRejectAPIView.as_view(),
        name="claim-reject",
    ),
    path(
        "claims/<int:claim_id>/request-changes/",
        ClaimRequestChangesAPIView.as_view(),
        name="claim-request-changes",
    ),
    path(
        "claims/<int:claim_id>/finalize/",
        ClaimFinalizeAPIView.as_view(),
        name="claim-finalize",
    ),
    path(
        "claims/<int:claim_id>/",
        ClaimDetailAPIView.as_view(),
        name="claim-detail",
    ),
]