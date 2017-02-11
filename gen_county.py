import re
from pprint import pprint
import requests


def make_request():
    """Make request to get events.php"""
    return requests.get('http://www.geneseecounty911.org/events.php').content


def find_events(text):
    """Find the active_events array in text and extra the data"""
    pattern = re.compile(
        r"events\[\d*\] = new Array\('(\w*)', '(\d*\/\d*)', '([\d:]*)[^A-Z]*([A-Z]*)', '([\d*.]*)', '(-?[\d.]*)', '([^']*)', '([^']*)")
    active_events = []
    for m in re.finditer(pattern, text):
        d = {
            'id': m.group(1),
            'date': m.group(2),
            'time': '{} {}'.format(m.group(3), m.group(4)),
            'latitude': m.group(5),
            'longitude': m.group(6),
            'address': m.group(7),
            'incident': m.group(8),
        }
        active_events.append(d)
    return active_events


def print_events():
    """Print The Events"""
    text = make_request()
    pprint(find_events(text))


if __name__ == '__main__':
    print_events()
