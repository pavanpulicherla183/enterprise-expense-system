"""
Admin configuration for claims application.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from claims.models import User, Claim, ClaimStatusHistory, AuditLog, Evidence, EvidenceReuseFlag

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for custom user model.
    """

    list_display = (
        "id",
        "email",
        "username",
        "role",
        "is_active",
        "created_at",
    )

    ordering = ("-created_at",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Role Information",
            {
                "fields": (
                    "role",
                    "created_at",
                ),
            },
        ),
    )

    readonly_fields = ("created_at",)

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    """
    Admin configuration for claims.
    """

    list_display = (
        "id",
        "employee",
        "status",
        "amount",
        "created_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "employee__email",
    )

@admin.register(ClaimStatusHistory)
class ClaimStatusHistoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for claim status history.
    """

    list_display = (
        "id",
        "claim",
        "old_status",
        "new_status",
        "changed_by",
        "changed_at",
    )

    list_filter = (
        "new_status",
    )

    readonly_fields = (
        "changed_at",
    )

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for audit logs.
    """

    list_display = (
        "id",
        "action",
        "actor",
        "claim",
        "timestamp",
    )

    readonly_fields = (
        "id",
        "claim",
        "actor",
        "action",
        "old_value",
        "new_value",
        "metadata",
        "timestamp",
    )

    def has_change_permission(self, request, obj=None):
        """
        Prevent modification of audit logs from admin.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of audit logs from admin.
        """
        return False

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    """
    Admin configuration for evidence files.
    """

    list_display = (
        "id",
        "claim",
        "file_name",
        "content_hash",
        "uploaded_by",
        "uploaded_at",
    )

    readonly_fields = (
        "content_hash",
        "uploaded_at",
    )

    search_fields = (
        "file_name",
        "content_hash",
    )

@admin.register(EvidenceReuseFlag)
class EvidenceReuseFlagAdmin(admin.ModelAdmin):
    """
    Admin configuration for evidence reuse flags.
    """

    list_display = (
        "id",
        "evidence",
        "primary_claim",
        "secondary_claim",
        "flagged_by",
        "resolved",
        "flagged_at",
    )

    list_filter = (
        "resolved",
    )

    readonly_fields = (
        "flagged_at",
    )