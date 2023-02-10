""" Module serializers providing django serializers"""
from rest_framework import serializers
from api.models import (
    Team, TeamMember, Happiness
)


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model
    """
    user = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=TeamMember.objects.all())

    class Meta:
        """
        Serializer fields
        """
        model = Team
        fields = ['name', 'user',]

class HappinessSerializer(serializers.ModelSerializer):
    """
    Serializer for Happiness model
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """
        Serializer fields
        """
        model = Happiness
        fields = ['id', 'owner', 'rating', 'created_at',]
