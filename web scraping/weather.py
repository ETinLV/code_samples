import json
from pprint import pprint

import requests
import sys
from bs4 import BeautifulSoup

WEATHER_URL = 'http://forecast.weather.gov/MapClick.php?'


def make_request(lat, lon):
    """Make the request to the weather website"""
    url = WEATHER_URL
    request = requests.get(url, params={'lat': lat, 'lon': lon})
    return request.content


def parse_content(content):
    """Create Beautiful Soup Object"""
    return BeautifulSoup(content, "html.parser")


def get_forecast(lat, lon):
    """Create forecast array"""
    content = make_request(lat, lon)
    soup = parse_content(content)
    forecast = soup.find_all(class_="forecast-tombstone")
    forecast_array = []
    for day in forecast:
        daily_forecast = format_daily_forecast(day)
        forecast_array.append(daily_forecast)
    if len(forecast_array):
        return forecast_array
    return []


def format_daily_forecast(day):
    """Compile all forecast data for a day"""
    d = {
        'time_period': day.find(class_='period-name').get_text(),
        'conditions': day.find(class_='short-desc').get_text(),
        'high': convert_temp(day.find(class_='temp temp-high')),
        'low': convert_temp(day.find(class_='temp temp-low'))
    }
    return json.dumps(d)


def convert_temp(temp):
    if temp:
        return temp.get_text().split(' ')[1] + 'F'
    return 'null'


if __name__ == '__main__':
    try:
        lat = sys.argv[1]
        lon = sys.argv[2]
    except IndexError:
        lat = '36.175'
        lon = '-115.1372'
    pprint(get_forecast(lat, lon))
