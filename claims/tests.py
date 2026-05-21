from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from claims.models import (
    Claim,
    ClaimStatus,
    Evidence,
    EvidenceReuseFlag,
    User,
    UserRole,
)


class BaseAPITestCase(APITestCase):
    """
    Base test configuration.
    """

    def setUp(self):
        """
        Create test users.
        """

        self.employee = User.objects.create_user(
            username="employee",
            email="employee@test.com",
            password="Test1234",
            role=UserRole.EMPLOYEE,
        )

        self.reviewer = User.objects.create_user(
            username="reviewer",
            email="reviewer@test.com",
            password="Test1234",
            role=UserRole.REVIEWER,
        )

        self.controller = User.objects.create_user(
            username="controller",
            email="controller@test.com",
            password="Test1234",
            role=UserRole.CONTROLLER,
        )
    
class ClaimCreationTests(BaseAPITestCase):
    """
    Claim creation test cases.
    """

    def test_employee_can_create_claim(self):
        """
        Employee should successfully create claim.
        """

        self.client.force_authenticate(
            user=self.employee,
        )

        payload = {
            "amount": "500.00",
            "description": "Travel reimbursement",
            "purpose": "Client meeting",
        }

        response = self.client.post(
            "/api/claims/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Claim.objects.count(),
            1,
        )

class ReviewerPermissionTests(BaseAPITestCase):
    """
    Reviewer workflow permission tests.
    """

    def test_employee_cannot_approve_claim(self):
        """
        Employee should not approve claims.
        """

        claim = Claim.objects.create(
            employee=self.employee,
            amount="500.00",
            description="Travel",
            purpose="Meeting",
            status=ClaimStatus.SUBMITTED,
        )

        self.client.force_authenticate(
            user=self.employee,
        )

        response = self.client.post(
            f"/api/claims/{claim.id}/approve/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

class ReviewerPermissionTests(BaseAPITestCase):
    """
    Reviewer workflow permission tests.
    """

    def test_employee_cannot_approve_claim(self):
        """
        Employee should not approve claims.
        """

        claim = Claim.objects.create(
            employee=self.employee,
            amount="500.00",
            description="Travel",
            purpose="Meeting",
            status=ClaimStatus.SUBMITTED,
        )

        self.client.force_authenticate(
            user=self.employee,
        )

        response = self.client.post(
            f"/api/claims/{claim.id}/approve/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
    
    def test_reviewer_can_approve_claim(self):
        """
        Reviewer should approve submitted claims.
        """

        claim = Claim.objects.create(
            employee=self.employee,
            amount="500.00",
            description="Travel",
            purpose="Meeting",
            status=ClaimStatus.SUBMITTED,
        )

        self.client.force_authenticate(
            user=self.reviewer,
        )

        response = self.client.post(
            f"/api/claims/{claim.id}/approve/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        claim.refresh_from_db()

        self.assertEqual(
            claim.status,
            ClaimStatus.APPROVED,
        )

class ControllerWorkflowTests(BaseAPITestCase):
    """
    Controller workflow tests.
    """

    def test_controller_can_finalize_claim(self):
        """
        Controller should finalize approved claims.
        """

        claim = Claim.objects.create(
            employee=self.employee,
            amount="500.00",
            description="Travel",
            purpose="Meeting",
            status=ClaimStatus.APPROVED,
        )

        self.client.force_authenticate(
            user=self.controller,
        )

        response = self.client.post(
            f"/api/claims/{claim.id}/finalize/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        claim.refresh_from_db()

        self.assertEqual(
            claim.status,
            ClaimStatus.FINALIZED,
        )