import logging
import time
import datetime

from django.core.management.base import BaseCommand

from data.requester import get_matches, get_fixtures


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logging.root.setLevel(logging.INFO)
        imported_date = datetime.date.today() - datetime.timedelta(days=1)
        while True:
            try:
                logging.info('Started import - matches')
                get_matches()
                today = datetime.date.today()
                if imported_date < today:
                    logging.info('Started import - fixtures')
                    get_fixtures()
                    imported_date = today
            except Exception as exc:
                logging.exception(exc)
            wait_time = 60*5
            logging.info(f'Import finished, waiting: {wait_time} s.')
            time.sleep(wait_time)
