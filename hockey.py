import datetime
import json
from pprint import pprint

import requests

STAT_URL = 'https://statsapi.web.nhl.com/api/v1/schedule'


def make_request():
    """Make the request to NHL website"""
    today = datetime.datetime.today()
    one_week_ago = (today - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    today = today.strftime('%Y-%m-%d')
    params = {'startDate': one_week_ago,
              'endDate': today,
              'expand': 'schedule.teams,schedule.linescore,'}
    return requests.get(STAT_URL, params=params).content


def parse_response(content):
    """Convert response to JSON Dict"""
    return json.loads(content)


def scores_for_today():
    """Get score's object for most recent day with games"""
    content = make_request()
    daily_scores_json = parse_response(content)
    todays_games = {}
    for date in daily_scores_json['dates'][::-1]:
        if date['games']:
            todays_games = date['games']
            break
    return todays_games


def make_scores_object():
    """Compile all scores for day"""
    scores = []
    all_scores = scores_for_today()
    for game in all_scores:
        d = {'away': make_team_obect(game['teams']['away']),
             'home': make_team_obect(game['teams']['home']),
             'venue': game['venue']['name'],
             'current_period': game['linescore']['currentPeriod'],
             'current_period_ordinal': game['linescore'].get('currentPeriodOrdinal', 'Scheduled'),
             'current_period_time_remaining': game['linescore'].get('currentPeriodTimeRemaining', "N/A")
        }
        scores.append(d)
    return scores


def make_team_obect(team):
    team_info = {'name': team['team']['name'],
                 'short_name': team['team']['shortName'],
                 'abbreviation': team['team']['abbreviation'],
                 'score': team['score']
                 }
    return team_info


def print_scores():
    scores = make_scores_object()
    if len(scores) == 0:
        scores = 'No Games Today'
    print(json.dumps(scores, indent=4))


if __name__ == '__main__':
    print_scores()
