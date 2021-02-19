from rest_framework import serializers

from data.models import Team, Subscription


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'external_id', 'name']
        read_only_fields = ['external_id', 'name']


class SubscriptionSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(read_only=True, many=True)

    class Meta:
        model = Subscription
        fields = ['notification_type', 'notification_route', 'teams', 'notification_url', 'notification_email']

    def create(self, validated_data):
        subscription = Subscription.objects.create(**validated_data)
        if 'teams' in self.initial_data:
            teams_ids = self.initial_data.get('teams')
            for team in teams_ids:
                subscription.teams.add(team)
        return subscription
