import logging
import time
from django.core.management.base import BaseCommand
import schedule

from data.jobs import notify_weekly_subscriptions, notify_daily_subscriptions, notify_live_subscriptions


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logging.root.setLevel(logging.INFO)

        schedule.every().monday.at('08:00').do(notify_weekly_subscriptions)
        schedule.every().day.at('08:00').do(notify_daily_subscriptions)
        schedule.every(5).minutes.do(notify_live_subscriptions)
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as exc:
                logging.exception(exc)
                time.sleep(10)
