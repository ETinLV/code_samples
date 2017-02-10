from pprint import pprint

import requests
import sys
from bs4 import BeautifulSoup

WEATHER_URL = 'http://forecast.weather.gov/MapClick.php?'


def make_request(lat,lon):
    """Make the request to the weather website"""
    url = WEATHER_URL + convert_lat_lon(lat, lon)
    request = requests.get(url)
    return request


def convert_lat_lon(lat, lon):
    """Format lat and lon values for query string"""
    lat_lon = 'lat={}&lon={}'.format(lat, lon)
    return lat_lon


def parse_content(request):
    """Create Beautiful Soup Object"""
    return BeautifulSoup(request.content, "html.parser")


def get_forecast(lat, lon):
    """Create forecast array"""
    soup = parse_content(make_request(lat, lon))
    forecast = soup.find_all(class_="forecast-tombstone")
    forecast_array = []
    for day in forecast:
        forecast_array.append(get_daily_forecast(day))
    if len(forecast_array) > 0:
        return forecast_array
    else:
        return "No information found for that location"


def get_daily_forecast(day):
    """Compile all forecast data for a day"""
    d = {}
    d['time_period'] = day.find(class_='period-name').get_text()
    d['conditions'] = day.find(class_='short-desc')
    d['high'] = day.find(class_='temp temp-high').get_text().split(' ')[1] + 'F' if day.find(
        class_='temp temp-high') else 'null'
    d['low'] = day.find(class_='temp temp-low').get_text().split(' ')[1] + 'F' if day.find(
        class_='temp temp-low') else 'null'
    return dict_to_utf_8(d)


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
    try:
        lat = sys.argv[1]
        lon = sys.argv[2]
    except IndexError:
        lat = '36.175'
        lon = '-115.1372'
    pprint(get_forecast(lat, lon))
