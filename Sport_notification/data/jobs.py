import datetime
import json

import requests
from data.models import Subscription, Fixture, Match
from django.db.models import Q


def notify_weekly_subscriptions():
    today = datetime.datetime.utcnow().date()
    start_datetime = datetime.datetime(today.year, today.month, today.day)
    end_datetime = start_datetime + datetime.timedelta(days=6)
    subscriptions = Subscription.objects.filter(notification_type=Subscription.Type.WEEK)
    for subscription in subscriptions:
        teams = subscription.teams.all()
        fixtures = Fixture.objects.filter(
            Q(team_one__in=teams) | Q(team_one__in=teams),
            start_datetime__range=(start_datetime, end_datetime)
        )
        notify_subscriber(subscription, fixtures)


def notify_daily_subscriptions():
    today = datetime.datetime.utcnow().date()
    start_datetime = datetime.datetime(today.year, today.month, today.day)
    subscriptions = Subscription.objects.filter(notification_type=Subscription.Type.DAY)
    for subscription in subscriptions:
        teams = subscription.teams.all()
        fixtures = Fixture.objects.filter(
            Q(team_one__in=teams) | Q(team_one__in=teams),
            start_datetime__date=today
        )
        notify_subscriber(subscription, fixtures)


def notify_live_subscriptions():
    start_datetime = datetime.datetime.now()
    subscriptions = Subscription.objects.filter(notification_type=Subscription.Type.LIVE)
    for subscription in subscriptions:
        last_update = subscription.sent or start_datetime - datetime.timedelta(minutes=5)
        teams = subscription.teams.filter(trigger=True)
        matches = Match.objects.filter(
            Q(team_one__in=teams) | Q(team_one__in=teams),
            last_changed__gte=last_update
        )
        notify_subscriber(subscription, matches)
        subscription.sent = start_datetime
        subscription.save(update_fields=['sent'])


def notify_subscriber(subscription, objects):
    if subscription.notification_route == Subscription.Route.HTTP_REQUEST:
        payload = format_http_route(objects)
        notify_through_url(payload, subscription.notification_url)
    elif subscription.notification_route == Subscription.Route.EMAIL:
        payload = format_email_route(objects)
        notify_through_email(payload, subscription.notification_email)
    else:
        raise NotImplementedError


def format_http_route(objects):
    data = []
    for obj in objects:
        data.append(obj.serialize())
    return json.dumps(data)


def format_email_route(objects):
    data = ""
    if objects.model is Match:
        for match in objects:
            data += match.email_format()
    elif objects.model is Fixture:
        for fixture in objects:
            data += fixture.email_format()
    return data


def notify_through_url(payload, url):
    #todo validate url somewhere
    if url and payload:
        pass
        # r = requests.request('POST', url, timeout=60, json=payload)


def notify_through_email(payload, email):
    with open('mail.txt', 'w') as file:
        file.write(payload)
