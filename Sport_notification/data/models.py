from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    trigger = models.BooleanField(default=False)
    #todo implement all fields for teams

    def notify_subscriptions(self):
        subscriptions = self.subscription_set
        for subscription in subscriptions:
            subscription.notify()


class Competition(models.Model):
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE)
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE)
    # todo implement all fields for competition

    def set_trigger(self):
        self.team_one.trigger = True
        self.team_two.trigger = True
        self.team_one.save()
        self.team_two.save()


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
    subscription = models.ForeignKey(Team, on_delete=models.CASCADE)
    #todo implement notify for different methods and different types

    def notify(self):
        pass


class Subscriber(User):
    subscription_details = models.ForeignKey(Subscription, on_delete=models.CASCADE)

