import datetime
import logging

import pytz
from django.conf import settings
import requests

from data.models import Match, Team, Fixture
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


def get_matches():
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
    matches = r.json().get('data', {}).get('match', [])
    for match in matches:
        external_id = match['id']
        formatted_item_matches = format_matches(match)
        try:
            existing_match = Match.objects.get(external_id=external_id)
        except ObjectDoesNotExist:
            team_one = create_team(match['home_id'], match['home_name'])
            team_two = create_team(match['away_id'], match['away_name'])
            new_match = Match.objects.create(
                external_id=external_id,
                team_one=team_one,
                team_two=team_two,
                **formatted_item_matches
            )
            new_match.set_trigger()
            logger.info('Created match')
        else:
            last_changed_raw = match.get('last_changed')
            last_changed_naive = datetime.datetime.strptime(last_changed_raw, '%Y-%m-%d %H:%M:%S')
            last_changed_aware = pytz.UTC.localize(last_changed_naive)
            if last_changed_aware > existing_match.last_changed:
                Match.objects.filter(pk=existing_match.pk).update(**formatted_item_matches)
                existing_match.set_trigger()
                logger.info('Updated match')
            else:
                logger.info('Match unchanged')


def format_matches(item):
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
        'score': item.get('score'),
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


def get_fixtures():
    params = {
        'key': settings.LIVE_SCORE_API_KEY,
        'secret': settings.LIVE_SCORE_API_SECRET,
    }
    url = 'http://livescore-api.com/api-client/fixtures/matches.json'
    date_today = datetime.date.today()
    for timedelta_days in range(0, 7):
        param_datetime = date_today + datetime.timedelta(days=timedelta_days)
        logger.info(f'Getting fixtures for date: {param_datetime.strftime("%Y-%m-%d")}')
        params['date'] = param_datetime.strftime('%Y-%m-%d')
        while url:
            r = requests.request('GET', url, params=params, timeout=60)
            try:
                r.raise_for_status()
            except requests.HTTPError as e:
                logger.exception(e)
            data = r.json().get('data', {})
            for fixture in data.get('fixtures', []):
                external_id = fixture['id']
                formatted_item_fixture = format_fixtures(fixture)
                team_one = create_team(fixture['home_id'], fixture['home_name'])
                team_two = create_team(fixture['away_id'], fixture['away_name'])
                formatted_item_fixture['team_one'] = team_one
                formatted_item_fixture['team_two'] = team_two
                fixture, created = Fixture.objects.update_or_create(
                    external_id=external_id,
                    defaults=formatted_item_fixture
                )
                logger.info(f'Fixture created: {created}')
            if data.get('next_page'):
                url = data.get('next_page')
                logger.info(f'Get next page: {url}')
                params = {}


def format_fixtures(fixture):
    start_time, start_date, start_datetime = None, None, None
    time_str = fixture.get('time')
    if time_str:
        start_time = datetime.datetime.strptime(time_str, '%H:%M:%S').time()
    date_str = fixture.get('date')
    if date_str:
        start_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    if start_time and start_date:
        start_datetime = datetime.datetime.combine(start_date, start_time)
    return {
        'start_datetime': pytz.UTC.localize(start_datetime) if start_datetime else None,
        'location': fixture.get('location'),
        'competition_id': fixture.get('competition_id'),
        'league_id': fixture.get('league_id'),
        'competition_name': fixture.get('competition', {}).get('name'),
        'league_name': fixture.get('league', {}).get('name'),
    }