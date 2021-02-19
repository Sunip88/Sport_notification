import logging

from django.contrib.auth.models import User
from django.db import models

logger = logging.getLogger(__name__)


class Team(models.Model):
    trigger = models.BooleanField(default=False)
    external_id = models.CharField(max_length=64)
    name = models.CharField(max_length=256)


class Match(models.Model):
    external_id = models.CharField(max_length=64)
    competition_id = models.CharField(max_length=64)
    league_id = models.CharField(max_length=64)
    competition_name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    scheduled = models.CharField(max_length=16)
    ht_score = models.CharField(max_length=64, null=True)
    ft_score = models.CharField(max_length=64, null=True)
    et_score = models.CharField(max_length=64, null=True)
    time = models.CharField(max_length=32, null=True)
    league_name = models.CharField(max_length=128, null=True)
    last_changed = models.DateTimeField(null=True)
    added = models.DateTimeField(null=True)
    status = models.CharField(max_length=32)
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_one')
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_two')

    def set_trigger(self):
        self.team_one.trigger = True
        self.team_two.trigger = True
        self.team_one.save(update_fields=['trigger'])
        self.team_two.save(update_fields=['trigger'])


class Fixture(models.Model):
    external_id = models.CharField(max_length=64)
    competition_id = models.CharField(max_length=64)
    competition_name = models.CharField(max_length=128)
    league_id = models.CharField(max_length=64)
    league_name = models.CharField(max_length=128, null=True)
    location = models.CharField(max_length=128)
    start_datetime = models.DateTimeField()
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='fixture_team_one')
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='fixture_team_two')


class Subscription(models.Model):
    class Type(models.TextChoices):
        WEEK = 'week'
        DAY = 'day'
        LIVE = 'live'

    class Route(models.TextChoices):
        HTTP_REQUEST = 'http'
        EMAIL = 'email'

    notification_type = models.CharField(max_length=32, choices=Type.choices)
    notification_route = models.CharField(max_length=32, choices=Route.choices)
    teams = models.ManyToManyField(Team)
    sent = models.DateTimeField(null=True)


class Subscriber(User):
    subscription_details = models.ForeignKey(Subscription, on_delete=models.CASCADE)

