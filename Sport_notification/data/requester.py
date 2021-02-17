import datetime
import logging

import pytz
from django.conf import settings
import requests

from data.models import Competition, Team
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


def get_competitions():
    params = {
        'key': settings.LIVE_SCORE_API_KEY,
        'secret': settings.LIVE_SCORE_API_SECRET,
    }
    url = 'http://livescore-api.com/api-client/scores/live.json'
    r = requests.request('GET', url, params=params, timeout=60)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        logger.exception(e)
    matches = r.json().get('data', {}).get('match')
    for match in matches:
        external_id = match['id']
        formatted_item_competition = format_competitions(match)
        try:
            existing_match = Competition.objects.get(external_id=external_id)
        except ObjectDoesNotExist:
            team_one = create_team(match['home_id'], match['home_name'])
            team_two = create_team(match['away_id'], match['away_name'])
            new_match = Competition.objects.create(
                external_id=external_id,
                team_one=team_one,
                team_two=team_two,
                **formatted_item_competition
            )
            new_match.set_trigger()
            logger.info('Created match')
        else:
            last_changed_raw = match.get('last_changed')
            last_changed_naive = datetime.datetime.strptime(last_changed_raw, '%Y-%m-%d %H:%M:%S')
            last_changed_aware = pytz.UTC.localize(last_changed_naive)
            if last_changed_aware > existing_match.last_changed:
                Competition.objects.filter(pk=existing_match.pk).update(**formatted_item_competition)
                existing_match.set_trigger()
                logger.info('Updated match')
            else:
                logger.info('Match unchanged')


def format_competitions(item):
    last_changed_raw = item.get('last_changed')
    last_changed = None
    if last_changed_raw:
        last_changed = datetime.datetime.strptime(last_changed_raw, '%Y-%m-%d %H:%M:%S')
    added_raw = item.get('last_changed')
    added = None
    if added_raw:
        added = datetime.datetime.strptime(added_raw, '%Y-%m-%d %H:%M:%S')

    return {
        'competition_id': item.get('competition_id'),
        'league_id': item.get('league_id'),
        'competition_name': item.get('competition_name'),
        'location': item.get('location'),
        'scheduled': item.get('scheduled'),
        'ht_score': item.get('ht_score'),
        'ft_score': item.get('ft_score'),
        'et_score': item.get('et_score'),
        'time': item.get('time'),
        'league_name': item.get('league_name'),
        'status': item.get('status'),
        'last_changed': pytz.UTC.localize(last_changed),
        'added': pytz.UTC.localize(added),
    }


def create_team(team_id, team_name):
    team, _ = Team.objects.get_or_create(
        external_id=team_id,
        name=team_name
    )
    return team
