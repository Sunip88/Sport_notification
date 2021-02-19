from data.models import Subscription


def notify_weekly_subscriptions():
    subscriptions = Subscription.objects.filter(notification_type=Subscription.Type.WEEK)
    for subscription in subscriptions:
        teams = subscription.teams.all()
        for team in teams:
            team


def notify_daily_subscriptions():
    subscriptions = Subscription.objects.filter(notification_type=Subscription.Type.DAY)
    for subscription in subscriptions:
        teams = subscription.teams.all()
        for team in teams:
            pass

def notify_live_subscriptions():
    subscriptions = Subscription.objects.filter(notification_type=Subscription.Type.LIVE)
    for subscription in subscriptions:
        teams = subscription.teams.all()
        for team in teams:
            pass