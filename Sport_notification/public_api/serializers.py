from rest_framework import serializers

from data.models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'external_id', 'name']