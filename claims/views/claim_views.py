"""
API views for claim workflows.
"""

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from claims.models.claim import ClaimStatus
from claims.serializers import ClaimCreateSerializer, EvidenceUploadSerializer
from claims.services.claim_service import ClaimService
from claims.selectors.claim_selector import (
    get_claim_by_id,
    get_claims_for_user,
)
from drf_spectacular.utils import extend_schema
from claims.permissions import IsEmployee, IsReviewer, IsController
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)

class ClaimCreateAPIView(ListAPIView, APIView):
    """
    API endpoint for creating and listing claims.
    """

    serializer_class = ClaimCreateSerializer
    permission_classes = [IsEmployee]

    def get_queryset(self):
        """
        Return claims visible to current user.
        """

        return get_claims_for_user(
            user=self.request.user,
        )

    @extend_schema(
        request=ClaimCreateSerializer,
        responses=ClaimCreateSerializer,
    )
    def post(self, request):
        """
        Create new claim.
        """

        serializer = ClaimCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        claim = ClaimService.create_claim(
            employee=request.user,
            validated_data=serializer.validated_data,
        )

        response_serializer = ClaimCreateSerializer(
            claim,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

class ClaimSubmitAPIView(APIView):
    """
    API endpoint for claim submission workflow.
    """

    permission_classes = [IsEmployee]

    def post(self, request, claim_id):
        """
        Submit claim into review workflow.
        """

        claim = get_claim_by_id(
            claim_id=claim_id,
        )

        updated_claim = ClaimService.submit_claim(
            claim=claim,
            employee=request.user,
        )

        serializer = ClaimCreateSerializer(
            updated_claim,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class EvidenceUploadAPIView(APIView):
    """
    API endpoint for uploading claim evidence.
    """

    permission_classes = [IsEmployee]
    parser_classes = [MultiPartParser]

    @extend_schema(
        request=EvidenceUploadSerializer,
        responses=EvidenceUploadSerializer,
    )
    def post(self, request, claim_id):
        """
        Upload evidence attachment.
        """

        claim = get_claim_by_id(
            claim_id=claim_id,
        )

        serializer = EvidenceUploadSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        evidence = ClaimService.upload_evidence(
            claim=claim,
            uploaded_by=request.user,
            uploaded_file=serializer.validated_data["file"],
        )

        response_serializer = EvidenceUploadSerializer(
            evidence,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

class ClaimApproveAPIView(APIView):
    """
    API endpoint for reviewer claim approval.
    """

    permission_classes = [IsReviewer]

    def post(self, request, claim_id):
        """
        Approve submitted claim.
        """

        claim = get_claim_by_id(
            claim_id=claim_id,
        )

        updated_claim = ClaimService.review_claim(
            claim=claim,
            reviewer=request.user,
            target_status=ClaimStatus.APPROVED,
            action="CLAIM_APPROVED",
        )

        serializer = ClaimCreateSerializer(
            updated_claim,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    
class ClaimRejectAPIView(APIView):
    """
    API endpoint for reviewer claim rejection.
    """

    permission_classes = [IsReviewer]

    def post(self, request, claim_id):
        """
        Reject submitted claim.
        """

        claim = get_claim_by_id(
            claim_id=claim_id,
        )

        updated_claim = ClaimService.review_claim(
            claim=claim,
            reviewer=request.user,
            target_status=ClaimStatus.REJECTED,
            action="CLAIM_REJECTED",
        )

        serializer = ClaimCreateSerializer(
            updated_claim,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class ClaimRequestChangesAPIView(APIView):
    """
    API endpoint for reviewer change requests.
    """

    permission_classes = [IsReviewer]

    def post(self, request, claim_id):
        """
        Request claim modifications.
        """

        claim = get_claim_by_id(
            claim_id=claim_id,
        )

        updated_claim = ClaimService.review_claim(
            claim=claim,
            reviewer=request.user,
            target_status=ClaimStatus.CHANGES_REQUESTED,
            action="CLAIM_CHANGES_REQUESTED",
        )

        serializer = ClaimCreateSerializer(
            updated_claim,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class ClaimFinalizeAPIView(APIView):
    """
    API endpoint for finance controller finalization.
    """

    permission_classes = [IsController]

    def post(self, request, claim_id):
        """
        Finalize approved claim.
        """

        claim = get_claim_by_id(
            claim_id=claim_id,
        )

        updated_claim = ClaimService.finalize_claim(
            claim=claim,
            controller=request.user,
        )

        serializer = ClaimCreateSerializer(
            updated_claim,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class ClaimListAPIView(ListAPIView):
    """
    API endpoint for listing claims.
    """

    serializer_class = ClaimCreateSerializer

    def get_queryset(self):
        """
        Return claims visible to current user.
        """

        return get_claims_for_user(
            user=self.request.user,
        )


class ClaimDetailAPIView(RetrieveAPIView):
    """
    API endpoint for claim details.
    """

    serializer_class = ClaimCreateSerializer
    lookup_url_kwarg = "claim_id"

    def get_queryset(self):
        """
        Return claims visible to current user.
        """

        return get_claims_for_user(
            user=self.request.user,
        )