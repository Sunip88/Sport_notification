import logging
import time
from django.core.management.base import BaseCommand

from data.requester import get_competitions


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logging.root.setLevel(logging.INFO)
        while True:
            try:
                logging.info('Started import')
                get_competitions()
            except Exception as exc:
                logging.exception(exc)
            wait_time = 60*5
            logging.info(f'Import finished, waiting: {wait_time} s.')
            time.sleep(wait_time)
