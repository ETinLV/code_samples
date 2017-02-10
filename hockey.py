import json
from datetime import datetime
from pprint import pprint

import requests


def make_request():
    """Make the request to NHL website"""
    return requests.get(
        'https://statsapi.web.nhl.com/api/v1/schedule?startDate=2017-02-09&endDate=2017-02-14&expand=schedule.teams,schedule.linescore,schedule.broadcasts.all,schedule.ticket,schedule.game.content.media.epg,schedule.radioBroadcasts,schedule.decisions,schedule.scoringplays,schedule.game.content.highlights.scoreboard,team.leaders,schedule.game.seriesSummary,seriesSummary.series&leaderCategories=points,goals,assists&leaderGameTypes=R&site=en_nhl&teamId=&gameType=&timecode=')


def parse_response():
    """Convert response to JSON Dict"""
    return json.loads(make_request().content)


def scores_for_today():
    """Get score's object for today"""
    today = datetime.today()
    daily_scores_json = parse_response()
    todays_games = {}
    for date in daily_scores_json['dates']:
        if datetime.strptime(date['date'], '%Y-%m-%d').date() == today.date():
            todays_games = date['games']
            break
        else:
            continue
    return todays_games


def make_scores_object():
    """Compile all scores for day"""
    scores = []
    all_scores = scores_for_today()
    for game in all_scores:
        d = {'venue': game['venue']['name'],
             'away': {
                 'name': game['teams']['away']['team']['name'],
                 'short_name': game['teams']['away']['team']['shortName'],
                 'abbreviation': game['teams']['away']['team']['abbreviation'],
                 'score': game['teams']['away']['score']
             },
             'home': {
                 'name': game['teams']['home']['team']['name'],
                 'short_name': game['teams']['home']['team']['shortName'],
                 'abbreviation': game['teams']['home']['team']['abbreviation'],
                 'score': game['teams']['home']['score']
             },
             'current_period': game['linescore']['currentPeriod'],
             'current_period_ordinal': game['linescore'].get('currentPeriodOrdinal', 'Scheduled'),
             'current_period_time_remaining': game['linescore'].get('currentPeriodTimeRemaining', "N/A")
             }
        scores.append(dict_to_utf_8(d))
    return scores


def print_scores():
    scores = make_scores_object()
    if len(scores) == 0:
        scores = 'No Games Today'
    pprint(scores)


def dict_to_utf_8(d):
    """Convert a dict with unicode to utf-8, this removes the u'' from printed text"""
    for k,v in d.iteritems():
        if isinstance(v, dict):
            dict_to_utf_8(v)
        new_k = k.encode('utf-8', 'ignore') if isinstance(k, unicode) else k
        d[new_k] = d.pop(k)
        d[k] = v.encode('utf-8', 'ignore') if isinstance(v, unicode) else v
    return d

if __name__ == '__main__':
    print_scores()
