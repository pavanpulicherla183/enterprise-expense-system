"""
Serializers for claim workflows.
"""

from rest_framework import serializers

from claims.models import Claim


class ClaimCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating expense claims.
    """

    class Meta:
        model = Claim

        fields = (
            "id",
            "amount",
            "description",
            "purpose",
            "status",
            "created_at",
        )

        read_only_fields = (
            "id",
            "status",
            "created_at",
        )