"""
Serializers for evidence workflows.
"""

from rest_framework import serializers

from claims.models import Evidence


class EvidenceUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading claim evidence.
    """

    class Meta:
        model = Evidence

        fields = (
            "id",
            "file",
            "file_name",
            "file_size",
            "mime_type",
            "uploaded_at",
        )

        read_only_fields = (
            "id",
            "file_name",
            "file_size",
            "mime_type",
            "uploaded_at",
        )

    def validate_file(self, value):
        """
        Validate uploaded file.
        """

        max_size = 10 * 1024 * 1024

        if value.size > max_size:
            raise serializers.ValidationError(
                "File size cannot exceed 10 MB."
            )

        allowed_types = [
            "application/pdf",
            "image/jpeg",
            "image/png",
        ]

        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Unsupported file type."
            )

        return value