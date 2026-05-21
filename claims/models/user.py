"""
Custom user model definitions for the enterprise expense system.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    """
    Enumeration for supported user roles.
    """

    EMPLOYEE = "EMPLOYEE", "Employee"
    REVIEWER = "REVIEWER", "Reviewer"
    CONTROLLER = "CONTROLLER", "Controller"


class User(AbstractUser):
    """
    Custom user model with role-based access support.
    """

    email = models.EmailField(
        unique=True,
    )

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.EMPLOYEE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        String representation of user.
        """
        return f"{self.email} ({self.role})"