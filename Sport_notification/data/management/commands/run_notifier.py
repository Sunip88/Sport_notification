import logging
import time
from django.core.management.base import BaseCommand

from data.models import Team


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logging.root.setLevel(logging.INFO)
        while True:
            try:
                logging.info('Checking triggers')
                teams = Team.objects.filter(trigger=True)
                for team in teams:
                    logging.info(f'Team {team.name} is triggered')
                    team.notify_subscriptions()
                teams.update(trigger=False)
            except Exception as exc:
                logging.exception(exc)
            wait_time = 60
            logging.info(f'Finished, waiting: {wait_time} s.')
            time.sleep(wait_time)
